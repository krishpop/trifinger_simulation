from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=[
        "trifinger_simulation",
        "trifinger_simulation.gym_wrapper",
        "trifinger_simulation.gym_wrapper.envs",
    ],
    package_dir={"": "python"},
    package_data={
        "": [
            "robot_properties_fingers/meshes/stl/*",
            "robot_properties_fingers/urdf/*",
        ]
    },
)

setup(**d)
