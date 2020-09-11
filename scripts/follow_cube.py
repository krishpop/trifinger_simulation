#!/usr/bin/env python3
"""Simple Inverse kinematics demo."""
import time

import numpy as np
import rospkg
import cv2
from scipy.spatial.transform import Rotation

import trifinger_simulation
import trifinger_simulation.collision_objects
import trifinger_simulation.finger_types_data
import trifinger_simulation.pinocchio_utils

import robot_interfaces
import robot_fingers

import trifinger_cameras
from trifinger_cameras.utils import convert_image


def sim():
    time_step = 0.004
    finger = trifinger_simulation.SimFinger(
        finger_type="trifingerpro",
        time_step=time_step,
        enable_visualization=True,
    )

    init_pos = np.array([0, 1.5, -2.7] * finger.number_of_fingers)
    finger.reset_finger_positions_and_velocities(init_pos)

    cube = trifinger_simulation.collision_objects.Block()

    joint_pos = init_pos
    while True:
        finger_action = finger.Action(position=joint_pos)
        t = finger.append_desired_action(finger_action)
        obs = finger.get_observation(t)

        goal = cube.get_state()[0]
        goal[2] += 0.06

        joint_pos, err = finger.kinematics.inverse_kinematics_one_finger(
            0,
            goal,
            obs.position
        )

        # keep the other two fingers up
        joint_pos[3:] = init_pos[3:]


def real():
    robot = robot_fingers.Robot.create_by_name("trifingerpro")
    if args.log:
        logger = robot_interfaces.trifinger.Logger(robot.robot_data, 100)
        logger.start(args.log)

    robot_properties_path = rospkg.RosPack().get_path(
        "robot_properties_fingers"
    )
    urdf_file = trifinger_simulation.finger_types_data.get_finger_urdf(
        "trifingerpro"
    )
    finger_urdf_path = os.path.join(
        robot_properties_path, "urdf", urdf_file
    )
    kinematics = trifinger_simulation.pinocchio_utils.Kinematics(
        finger_urdf_path,
        ["finger_tip_link_0", "finger_tip_link_120", "finger_tip_link_240"],
    )

    camera_data = trifinger_cameras.tricamera.SingleProcessData()
    camera_driver = trifinger_cameras.tricamera.TriCameraDriver(
        "camera60", "camera180", "camera300", downsample_images=False,
    )
    camera_backend = trifinger_cameras.tricamera.Backend(  # noqa
        camera_driver, camera_data
    )
    camera_frontend = trifinger_cameras.tricamera.Frontend(camera_data)

    # ArUco stuff
    marker_dict = cv2.aruco.getPredefinedDictionary(
        cv2.aruco.DICT_APRILTAG_16h5
    )
    marker_length = 0.04
    marker_id = 0
    # FIXME
    camera_matrix60 = None
    dist_coeffs60 = None

    robot.initialize()

    init_pos = np.array([0, 1.5, -2.7] * finger.number_of_fingers)

    for i in range(500):
        finger_action = robot_interfaces.trifinger.Action(position=init_pos)
        robot.frontend.append_desired_action(finger_action)

    while True:
        finger_action = robot_interfaces.trifinger.Action(position=joint_pos)
        t = robot.frontend.append_desired_action(finger_action)
        obs = robot.frontend.get_observation(t)

        images = camera_frontend.get_latest_observation()
        img60 = convert_image(images.cameras[0].image)

        marker_corners, ids, _ = cv2.aruco.detectMarkers(img60, marker_dict)
        try:
            i = ids.index(marker_id)
        except ValueError:
            # marker not detected
            time.sleep(0.1)
            continue

        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            marker_corners, marker_length, camera_matrix60, dist_coeffs60)

        rvec = rvecs[i]
        tvec = tvec[i]

        #rot = Rotation.from_rotvec(rvec)

        # TODO: transform marker position to world frame
        world_marker_position = None

        print("Marker position:", world_marker_position)

        # set goal a bit above the marker
        goal = world_marker_position
        goal[2] += 0.03

        joint_pos, err = kinematics.inverse_kinematics_one_finger(
            0,
            goal,
            obs.position
        )
        # keep the other two fingers up
        joint_pos[3:] = init_pos[3:]


if __name__ == "__main__":
    sim()