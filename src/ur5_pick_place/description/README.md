# description/

URDF/Xacro files for the arm, gripper, and scene live here.

Per the M1 daily plan (Tue Sep 22 / Wed Sep 23 steps, adjust to your actual start date):

1. Clone the UR5 description into a scratch spot and copy/adapt the xacro into this folder:
   ```
   git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git /tmp/ur_description
   cp /tmp/ur_description/urdf/ur.urdf.xacro ./ur5_pick_place.urdf.xacro
   ```
2. Add a `<ros2_control>` block (joint interfaces) and the `gazebo_ros2_control` plugin reference to the xacro.
3. In M3, add the gripper xacro (e.g. a Robotiq 2F-85 description) and attach it at the arm's tool0 link.

Nothing is vendored here yet — this is an empty placeholder so `colcon build` has a stable install path from day one.
