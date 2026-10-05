# Project 1 — Pick-and-place with a simulated arm (ROS2 Humble, Docker)

This is the Humble/Docker environment for Project 1, kept as the fallback path
alongside the native Jazzy setup. Use this container if the native Jazzy
MoveIt2 binaries hit a packaging gap (see the M2 note in the Daily Plan doc),
or simply as your primary environment if you'd rather develop entirely inside
Humble.

## Layout

```
ur5_pick_place_ws/
├── docker/
│   ├── Dockerfile          # ROS2 Humble + Gazebo Classic + MoveIt2
│   ├── docker-compose.yml  # build/run with GUI (RViz2, Gazebo) support
│   ├── entrypoint.sh       # sources ROS2 + the workspace overlay
│   └── .dockerignore
└── src/
    └── ur5_pick_place/     # the ROS2 package (matches the layout in the plan doc)
        ├── package.xml
        ├── setup.py / setup.cfg
        ├── description/    # URDF/Xacro (vendor the UR5 xacro here — M1)
        ├── moveit_config/  # MoveIt Setup Assistant output goes here — M2
        ├── bringup/launch/ # bringup.launch.py — M1/M2
        ├── ur5_pick_place/ # Python package: pick_place_node.py — M4
        ├── config/         # poses.yaml — M5
        └── NOTES.md        # daily log, matches the Daily Plan doc's checklist
```

## One-time host setup (Ubuntu 24.04)

Install Docker + Compose if not already present:

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER   # log out/in after this
```

Allow the container to open GUI windows (RViz2, Gazebo) on your desktop:

```bash
xhost +local:docker
```
(Re-run this after every host reboot/login — it's not persistent by design.)

## Build and run

```bash
cd ur5_pick_place_ws/docker
docker compose build
docker compose run --rm ros2_humble
```

You'll land in a bash shell inside the container at `/ws`, with `src/`
live-mounted from your host (`ur5_pick_place_ws/src/`) — edits made on the
host with VSCode show up instantly inside the container.

Inside the container, first time only:

```bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

After that, each new shell into the running container just needs:

```bash
source install/setup.bash
```

## Quick smoke test

```bash
# Gazebo opens a window on your host desktop if xhost was set up correctly
gazebo
```

If a Gazebo window appears with no X11/DISPLAY errors in the terminal, the
GUI bridge is working and you're ready to start M1's Tuesday tasks (see the
Daily Plan doc).

## Reopening the container later

The named volumes (`ros2_build_cache`, `ros2_install_cache`, `ros2_log_cache`)
persist your `colcon build` output between runs, so you don't need to rebuild
from scratch each session:

```bash
cd ur5_pick_place_ws/docker
docker compose run --rm ros2_humble
# then just: source install/setup.bash
```

## Next steps (from the Daily Plan doc)

- M1 (Tue): `apt list --installed | grep ros-humble-desktop` to sanity-check the image, then vendor the UR5 xacro into `src/ur5_pick_place/description/` (see the README there).
- M2: run `ros2 run moveit_setup_assistant moveit_setup_assistant` from inside the container.
- Keep `NOTES.md` updated at the end of each day — it's the thing that makes progress traceable when you look back at the week.
