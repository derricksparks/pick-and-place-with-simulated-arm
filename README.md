# UR5 Pick-and-Place — ROS 2 Humble · MoveIt 2 · Gazebo

A simulated Universal Robots UR5 that picks cubes of different sizes and places them at target
poses, using MoveIt 2 for motion planning and `ros2_control` for joint control. It is the first
project in a five-part portfolio on industrial robot software.

<!-- TODO: replace with a real GIF once M4 (pick-place node) runs end to end -->
<!-- ![demo](docs/demo.gif) -->

## Status

| Milestone | What it delivers | Status |
|-----------|------------------|--------|
| M1 | UR5 spawned in Gazebo Classic, driven through `ros2_control`, Dockerized Humble environment | ✅ Done |
| M2 | MoveIt 2 config generated with the Setup Assistant; plans executing in RViz | ⏳ Next |
| M3 | Gripper + cubes in the world; collision objects in the planning scene | ⬜ |
| M4 | `pick_place_node.py`: approach → grasp → lift → move → place → retreat | ⬜ |
| M5 | Pick/place poses loaded from `config/poses.yaml`; several cube sizes | ⬜ |
| Stretch | Cube pose from a simulated camera instead of fixed poses | ⬜ |

## Architecture

```
            poses.yaml
                │
                ▼
     ┌─────────────────────┐   MoveGroup action    ┌──────────────┐
     │  pick_place_node    │ ────────────────────▶ │  move_group  │  (MoveIt 2)
     │  (Python, rclpy)    │ ◀──────────────────── │              │
     └─────────────────────┘     plan / result     └──────┬───────┘
                                                          │ FollowJointTrajectory
                                                          ▼
                                             ┌──────────────────────────┐
                                             │ joint_trajectory_        │
                                             │ controller (ros2_control)│
                                             └────────────┬─────────────┘
                                                          ▼
                                              Gazebo Classic (UR5 + cubes)
```

## Repository layout

```
ur5_pick_place_ws/
├── docker/                 # Humble + Gazebo Classic + MoveIt 2 image, compose file with GUI support
└── src/
    └── ur5_pick_place/
        ├── description/    # scene URDF/Xacro that includes the UR5 macro
        ├── moveit_config/  # MoveIt Setup Assistant output (M2)
        ├── bringup/launch/ # bringup.launch.py
        ├── ur5_pick_place/ # Python package: pick_place_node.py (M4)
        ├── config/         # poses.yaml (M5)
        └── NOTES.md        # development log
```

The UR arm model (URDF, meshes, kinematics) is not copied into this repo. It comes from the
upstream `ur_description` package, installed as the `ros-humble-ur-description` apt package
in the Docker image and declared as a dependency in `package.xml`.

## Quick start (Docker)

Requires Docker with the Compose plugin on an Ubuntu host.

```bash
# allow the container to open RViz/Gazebo windows (re-run after each login)
xhost +local:docker

git clone https://github.com/derricksparks/pick-and-place-with-simulated-arm.git ur5_pick_place_ws
cd ur5_pick_place_ws/docker
docker compose build
docker compose run --rm ros2_humble
```

Inside the container (first run only):

```bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Launch the simulation:

```bash
ros2 launch ur5_pick_place bringup.launch.py
```

This starts Gazebo, spawns the arm and brings up `joint_state_broadcaster` and
`joint_trajectory_controller`. The launch file takes no arguments.

`src/` is bind-mounted from the host, so edits made in VS Code show up immediately in the
container. Build output is kept in named volumes, so later sessions only need
`source install/setup.bash`.

## Design notes

- **Why Docker + Humble:** the host runs Ubuntu 24.04, whose native ROS 2 distro is Jazzy.
  Humble (LTS, still the most common distro in industrial job postings) runs in a container
  instead of being forced onto an unsupported OS.
- **Why `ros2_control` from M1:** real UR arms are driven through `ros2_control` by the official
  `ur_robot_driver`. Using the same controller interface in simulation means the planning code
  should not need to change when it moves to real hardware.
- **Gazebo Classic:** chosen for its mature `gazebo_ros2_control` integration on Humble. It has
  reached end-of-life, so migrating to modern Gazebo (`gz_ros2_control`) is a planned follow-up.

## Roadmap context

This is project 1 of 5: pick-and-place → custom `ros2_control` hardware interface → multi-robot
cell → digital twin with an OPC-UA bridge → sim-to-real with MuJoCo.

## License

Project code: MIT (see [LICENSE](LICENSE)). The UR description files and meshes are not part of
this repo; they are installed from the upstream
[Universal_Robots_ROS2_Description](https://github.com/UniversalRobots/Universal_Robots_ROS2_Description)
package and keep its license.
