"""
M2: MoveIt 2 planning for the UR5e in Gazebo Classic.

Starts the M1 simulation (ur5_pick_place bringup.launch.py: Gazebo, the arm,
joint_state_broadcaster, joint_trajectory_controller), then move_group and,
optionally, RViz with the MotionPlanning panel.

Flow: RViz or a node asks move_group for a plan -> move_group plans with OMPL
or Pilz -> sends the trajectory to joint_trajectory_controller's
FollowJointTrajectory action (see config/moveit_controllers.yaml) -> the
controller drives the joints in Gazebo.

This file lives in the MoveIt config package rather than in ur5_pick_place
because this package already depends on ur5_pick_place (for the robot
description); the reverse dependency would make a cycle colcon cannot build.

Run (after `colcon build --symlink-install && source install/setup.bash`):
    ros2 launch ur5_pick_place_moveit_config moveit_gazebo.launch.py
    ros2 launch ur5_pick_place_moveit_config moveit_gazebo.launch.py rviz:=false
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    rviz_arg = DeclareLaunchArgument(
        "rviz", default_value="true", description="Open RViz with the MotionPlanning panel")

    # Loads everything the Setup Assistant generated: the robot description
    # (from .setup_assistant -> ur5_pick_place/description/ur5_pick_place.urdf.xacro),
    # the SRDF, kinematics.yaml, joint_limits.yaml, the planning pipelines
    # (OMPL, Pilz, CHOMP) and moveit_controllers.yaml.
    # The xacro is loaded without the Gazebo arguments on purpose: that is the
    # model the SRDF (groups, collision matrix) was generated from. The joints
    # are identical to the Gazebo model; only the ros2_control block and the
    # Gazebo ground plane differ, and move_group uses neither.
    moveit_config = MoveItConfigsBuilder(
        "ur5_pick_place", package_name="ur5_pick_place_moveit_config"
    ).to_moveit_configs()

    # Gazebo publishes simulated time on /clock. Every node that reads
    # timestamps must use it, or trajectories look like they are in the past.
    sim_time = {"use_sim_time": True}

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ur5_pick_place"),
                "bringup", "launch", "bringup.launch.py")
        )
    )

    # move_group: the MoveIt server. Plans on request and executes the result
    # through the controller listed in moveit_controllers.yaml.
    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict(), sim_time],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d", str(moveit_config.package_path / "config" / "moveit.rviz")],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
            sim_time,
        ],
        condition=IfCondition(LaunchConfiguration("rviz")),
    )

    return LaunchDescription([
        rviz_arg,
        simulation,
        move_group,
        rviz,
    ])
