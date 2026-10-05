#!/bin/bash
set -e

# Source the base ROS2 Humble environment
source /opt/ros/humble/setup.bash

# Source the workspace overlay once it's been built
if [ -f /ws/install/setup.bash ]; then
    source /ws/install/setup.bash
fi

exec "$@"
