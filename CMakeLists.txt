cmake_minimum_required(VERSION 3.5)
project(trifinger_simulation)

# Specify C++ Standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED on)


find_package(ament_cmake REQUIRED)
find_package(mpi_cmake_modules REQUIRED)


ament_python_install_package(${PROJECT_NAME} PACKAGE_DIR python/${PROJECT_NAME})


add_doxygen_documentation()


# Installation
install_scripts(
    demos/demo_cameras.py
    demos/demo_control.py
    demos/demo_inverse_kinematics.py
    demos/demo_load_gym_env.py
    demos/demo_plain_torque_control.py
    demos/demo_random_policy.py
    demos/demo_trifinger_platform.py

    scripts/check_position_control_accuracy.py
    scripts/evaluate_policy.py
    scripts/profiling.py
    scripts/replay_action_log.py
    scripts/rrc_evaluate
    scripts/run_evaluate_policy_all_levels.py
    scripts/run_replay_all_levels.py

    DESTINATION lib/${PROJECT_NAME}
)


# Tests
if (BUILD_TESTING)
    find_package(ament_cmake_nose REQUIRED)

    # Python tests
    ament_add_nose_test(test_cube_env tests/test_cube_env.py)
    ament_add_nose_test(test_determinism tests/test_determinism.py)
    ament_add_nose_test(test_loading_urdfs tests/test_loading_urdfs.py)
    ament_add_nose_test(test_parallel_instances tests/test_parallel_instances.py)
    ament_add_nose_test(test_reset_joints tests/test_reset_joints.py)
    ament_add_nose_test(test_robot_equivalent_interface tests/test_robot_equivalent_interface.py)
    ament_add_nose_test(test_sample tests/test_sample.py)
    ament_add_nose_test(test_tasks_move_cube tests/test_tasks_move_cube.py)
    ament_add_nose_test(test_trifinger_platform tests/test_trifinger_platform.py)

endif()


ament_package()
