#!/usr/bin/env python3
"""Simple Inverse kinematics demo."""
import argparse
import time
import os

import numpy as np
import rospkg
import cv2
import yaml

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
            0, goal, obs.position
        )

        # keep the other two fingers up
        joint_pos[3:] = init_pos[3:]


def to_matrix(data: dict, key: str) -> np.ndarray:
    return np.array(data[key]["data"]).reshape(data[key]["rows"], data[key]["cols"])


class ArucoDetector:

    def __init__(self, calibration_file):
        # ArUco stuff
        self.marker_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
        self.marker_length = 0.04
        self.marker_id = 0

        with open(calibration_file, "r") as fh:
            camera_calib = yaml.load(fh)

        self.camera_matrix = to_matrix(camera_calib, "camera_matrix")
        self.dist_coeffs = to_matrix(camera_calib, "distortion_coefficients")
        self.trans_world_to_cam = to_matrix(camera_calib, "projection_matrix")
        self.trans_cam_to_world = np.linalg.inv(self.trans_world_to_cam)

    def detect_marker_pose(self, image):
        marker_corners, ids, _ = cv2.aruco.detectMarkers(image, self.marker_dict)
        try:
            i = np.where(ids == self.marker_id)[0][0]
        except Exception:
            return None

        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            marker_corners, self.marker_length, self.camera_matrix, self.dist_coeffs
        )

        # transform marker position from camera to world frame
        cam_marker_position = np.ones(4)
        cam_marker_position[:3] = tvecs[i]
        world_marker_position = self.trans_cam_to_world @ cam_marker_position

        return world_marker_position


def real():
    camera_names = ["camera60", "camera180", "camera300"]

    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument("camera_calib60")
    argparser.add_argument("camera_calib180")
    argparser.add_argument("camera_calib300")
    argparser.add_argument("--camera-name", "-c", choices=camera_names)
    args = argparser.parse_args()

    robot = robot_fingers.Robot.create_by_name("trifingerpro")

    robot_properties_path = rospkg.RosPack().get_path("robot_properties_fingers")
    urdf_file = trifinger_simulation.finger_types_data.get_finger_urdf("trifingerpro")
    finger_urdf_path = os.path.join(robot_properties_path, "urdf", urdf_file)
    kinematics = trifinger_simulation.pinocchio_utils.Kinematics(
        finger_urdf_path,
        ["finger_tip_link_0", "finger_tip_link_120", "finger_tip_link_240"],
    )

    if args.camera_name:
        camera_index = camera_names.index(args.camera_name)
    else:
        camera_index = None

    camera_data = trifinger_cameras.tricamera.SingleProcessData()
    camera_driver = trifinger_cameras.tricamera.TriCameraDriver(
        *camera_names,
        downsample_images=False,
    )
    camera_backend = trifinger_cameras.tricamera.Backend(  # noqa
        camera_driver, camera_data
    )
    camera_frontend = trifinger_cameras.tricamera.Frontend(camera_data)

    detectors = [
        ArucoDetector(args.camera_calib60),
        ArucoDetector(args.camera_calib180),
        ArucoDetector(args.camera_calib300),
    ]

    robot.initialize()

    init_pos = np.array([0, 1.5, -2.7] * 3)

    for i in range(500):
        finger_action = robot_interfaces.trifinger.Action(position=init_pos)
        robot.frontend.append_desired_action(finger_action)

    joint_pos = init_pos
    i = 0
    while True:
        i += 1

        finger_action = robot_interfaces.trifinger.Action(position=joint_pos)
        finger_action.position_kp = [8] * 9
        finger_action.position_kd = [0.01] * 9
        t = robot.frontend.append_desired_action(finger_action)
        obs = robot.frontend.get_observation(t)

        images = camera_frontend.get_latest_observation()

        if camera_index is not None:
            img = convert_image(images.cameras[camera_index].image)
            world_marker_position = detectors[camera_index].detect_marker_pose(img)

            if world_marker_position is None:
                time.sleep(0.1)
                continue
        else:
            positions = [
                detector.detect_marker_pose(convert_image(camera.image))
                for detector, camera in zip(detectors, images.cameras)
            ]
            # filter out Nones
            positions = [p for p in positions if p is not None]
            if not positions:
                time.sleep(0.1)
                continue

            world_marker_position = np.mean(positions, axis=0)


        # set goal a bit above the marker
        goal = np.array(world_marker_position[:3], copy=True)
        goal[2] += 0.06

        new_joint_pos, err = kinematics.inverse_kinematics_one_finger(
            0, goal, obs.position, tolerance=0.002, max_iterations=3000)

        # keep the other two fingers up
        alpha = 0.1
        joint_pos[:3] = alpha * new_joint_pos[:3] + (1 - alpha) * joint_pos[:3]

        if i % 500 == 0:
            tip_pos = kinematics.forward_kinematics(obs.position)

            print("-----------------------------------------------------")
            print("Marker position:", np.round(world_marker_position[:3], 3))
            print("Tip goal:", np.round(goal, 3))
            print("Tip position:", np.round(tip_pos[0], 3))
            print("IK error:", np.round(err, 3))


if __name__ == "__main__":
    real()
