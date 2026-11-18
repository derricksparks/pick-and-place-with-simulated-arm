"""
M1 bring-up: Gazebo Classic + robot_state_publisher + spawn the UR5e +
joint_state_broadcaster + joint_trajectory_controller.

The robot comes from this package's description/ur5_pick_place.urdf.xacro,
which wraps ur_description's UR macro. With sim_gazebo:=true the macro also
generates the <ros2_control> tag and the Gazebo plugin block.

Run (after `colcon build --symlink-install && source install/setup.bash`):
    ros2 launch ur5_pick_place bringup.launch.py
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    ur5_pick_place_share = get_package_share_directory("ur5_pick_place")
    gazebo_ros_share = get_package_share_directory("gazebo_ros")

    robot_xacro = os.path.join(ur5_pick_place_share, "description", "ur5_pick_place.urdf.xacro")
    controllers_yaml = os.path.join(ur5_pick_place_share, "config", "ur5_controllers.yaml")

    # Build the robot_description param by running xacro on the project's own
    # description (the same file the MoveIt config uses). Name and ur_type
    # come from the file's defaults; sim_gazebo + simulation_controllers make
    # the UR macro emit the Gazebo <ros2_control> block and plugin.
    robot_description_content = Command([
        "xacro ", robot_xacro,
        " sim_gazebo:=true",
        " simulation_controllers:=", controllers_yaml,
    ])
    robot_description = {
        "robot_description": ParameterValue(
            robot_description_content,
            value_type=str)}

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, "launch", "gazebo.launch.py")
        )
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "ur5_pick_place"],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    joint_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller"],
        output="screen",
    )

    # Order matters: spawn_entity has to finish before the controller
    # spawners can find the controller_manager the Gazebo plugin started,
    # and joint_state_broadcaster should come up before the trajectory
    # controller. Chain them with event handlers instead of a fixed sleep.
    delay_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_state_broadcaster_spawner],
        )
    )
    delay_joint_trajectory_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[joint_trajectory_controller_spawner],
        )
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        delay_joint_state_broadcaster,
        delay_joint_trajectory_controller,
    ])
