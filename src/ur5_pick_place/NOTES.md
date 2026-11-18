# Project 1 notes log

Short, dated entries — matches the "update NOTES.md" step at the end of each day
in the Daily Plan doc. Keep each entry to 2-3 lines: what worked, what to fix.

## Template

### YYYY-MM-DD — M<n>, Day
- What got done:
- What's broken / open:
- Next step:

### 2026-11-18 — M2
- What got done: MoveIt config from the Setup Assistant (`ur5_pick_place_moveit_config`).
  Fixed what the GUI didn't save (group name, home pose, controller joints) and added
  acceleration limits. `moveit_gazebo.launch.py` runs Gazebo + move_group + RViz; plans
  from RViz execute on the Gazebo arm.
- Lessons: xacro copies comments into the URDF, and a colon followed by a space breaks
  gazebo_ros2_control's parameter parsing. A stale `install/` overlay can override apt
  packages: clean it, then start a fresh shell.
- What's broken / open: MoveIt doesn't know about the floor yet. KDL IK sometimes fails on
  reachable poses. `setup.cfg` deprecation warning.
- Next step: M3, gripper + cubes + planning scene.
