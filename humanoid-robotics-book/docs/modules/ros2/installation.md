---
sidebar_position: 2
---

# ROS 2 Installation Guide

## Overview

This guide will help you install ROS 2 Humble Hawksbill on Ubuntu 22.04, which is the recommended setup for working with humanoid robots. ROS 2 Humble is an LTS (Long Term Support) release that will be supported until May 2027, making it ideal for long-term projects.

## System Requirements

- **Operating System**: Ubuntu 22.04 (Jammy Jellyfish)
- **RAM**: At least 8GB (16GB recommended for simulation)
- **Disk Space**: At least 10GB available
- **Processor**: Multi-core processor (Intel i5 or equivalent AMD)

## Installation Steps

### 1. Set Locale

First, ensure your locale is set appropriately:

```bash
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8
```

### 2. Setup Sources

Add the ROS 2 repository to your system:

```bash
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
```

Create the repository entry:

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### 3. Install ROS 2 Packages

Update your package list and install the desktop variant of ROS 2 Humble:

```bash
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install ros-dev-tools
```

The `desktop` variant includes everything in `ros-base` plus additional packages for common robot applications, including GUI tools and 2D/3D simulators.

### 4. Environment Setup

To use ROS 2, you need to source the setup files in every terminal where you use ROS 2. Add the following line to your `~/.bashrc` file:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

For a single terminal session (without modifying `.bashrc`):

```bash
source /opt/ros/humble/setup.bash
```

### 5. Verify Installation

Test that ROS 2 is installed correctly by running the talker/listener demo:

In one terminal:
```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

In another terminal:
```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

You should see the talker publishing messages and the listener receiving them.

## Additional Tools

### Install Colcon (Package Build Tool)

Colcon is used to build ROS 2 packages:

```bash
pip3 install -U colcon-common-extensions
```

### Install RViz

RViz is the 3D visualization tool for ROS:

```bash
sudo apt install ros-humble-rviz2
```

### Install URDF Tools

For robot modeling and visualization:

```bash
sudo apt install ros-humble-urdf
sudo apt install ros-humble-xacro
```

## Troubleshooting

### Gazebo Issues

ROS 2 Humble comes with Ignition Fortress as the simulation backend. If you encounter issues with simulation:

```bash
sudo apt install ignition-fortress
```

### Python Path Issues

If you encounter Python import errors, ensure your Python packages are in the path:

```bash
export PYTHONPATH=/opt/ros/humble/lib/python3.10/site-packages:$PYTHONPATH
```

## Development Workspace Setup

Create a workspace for your ROS 2 development:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Next Steps

After completing the installation, you can:

1. Proceed to the [Nodes and Communication](./nodes.md) section
2. Set up your first ROS 2 workspace
3. Create simple publisher and subscriber nodes

## Alternative Installation Methods

For other platforms or installation methods, see the [official ROS 2 installation guide](https://docs.ros.org/en/humble/Installation.html).

---

## Verification Checklist

- [ ] ROS 2 Humble installed successfully
- [ ] Talker/listener demo runs without errors
- [ ] Colcon installed and working
- [ ] RViz installed and functional
- [ ] URDF and XACRO tools installed

## References

- [ROS 2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation.html)
- [Ubuntu Installation Guide](https://ubuntu.com/tutorials/install-ubuntu-desktop)
- [ROS 2 Environment Setup](https://docs.ros.org/en/humble/Tutorials/Configuring-ROS2-Environment.html)