import os
from glob import glob
from setuptools import find_packages, setup

package_name = "ur5_pick_place"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        # Launch files
        (os.path.join("share", package_name, "bringup", "launch"),
         glob("bringup/launch/*.launch.py")),
        # URDF / Xacro description files (vendor the UR5 xacro here in M1)
        (os.path.join("share", package_name, "description"),
         glob("description/*")),
        # Pose / scene config used in M5
        (os.path.join("share", package_name, "config"),
         glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Drake Grace",
    maintainer_email="drakegraceblessing@gmail.com",
    description="Project 1: pick-and-place with a simulated UR5 arm, planned with MoveIt 2 in Gazebo.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "pick_place_node = ur5_pick_place.pick_place_node:main",
        ],
    },
)
