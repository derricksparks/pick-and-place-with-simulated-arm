# ROS2 Humble container for Project 1 (Pick-and-place with simulated arm).
# Base: official OSRF image with full desktop tools (RViz2 included).
FROM osrf/ros:humble-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble

# --- Core build / dev tooling -------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    curl \
    vim \
    nano \
    build-essential \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    && rm -rf /var/lib/apt/lists/*

# --- Simulation: Gazebo Classic (the standard Humble pairing) ----------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-gazebo-plugins \
    && rm -rf /var/lib/apt/lists/*

# --- Control stack -------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-xacro \
    && rm -rf /var/lib/apt/lists/*

# --- Motion planning: MoveIt 2 --------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-moveit \
    ros-humble-moveit-planners-ompl \
    ros-humble-moveit-kinematics \
    ros-humble-moveit-setup-assistant \
    && rm -rf /var/lib/apt/lists/*

# --- rosdep init (ok if already initialized in the base image) ---------------
RUN rosdep update || true

# --- Workspace -------------------------------------------------------------
ENV WS=/ws
RUN mkdir -p ${WS}/src
WORKDIR ${WS}

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
