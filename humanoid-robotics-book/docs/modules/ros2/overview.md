---
sidebar_position: 1
---

# ROS 2 Fundamentals

## Overview

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

This module covers the foundational concepts of ROS 2 that are essential for controlling humanoid robots:

- **Nodes**: The fundamental unit of computation
- **Topics**: Communication channels for data streams
- **Services**: Request/response communication patterns
- **Actions**: Goal-oriented communication for long-running tasks
- **Parameters**: Configuration values for nodes
- **Launch files**: Mechanisms to start multiple nodes at once

## Learning Objectives

After completing this module, you will be able to:

- Understand the architecture of ROS 2 and how nodes communicate
- Create ROS 2 packages, nodes, publishers, and subscribers
- Design robot models using URDF (Unified Robot Description Format)
- Visualize robots in RViz (Robot Visualizer)
- Send commands from AI agents through ROS 2

## Module Structure

1. [Installation Guide](./installation.md) - Setting up ROS 2 Humble Hawksbill
2. [Nodes and Communication](./nodes.md) - Understanding ROS 2 nodes, topics, and services
3. [URDF and Robot Modeling](./urdf.md) - Creating robot models with URDF and XACRO
4. [Examples](./examples.md) - Practical examples and exercises

## Prerequisites

Before starting this module, ensure you have:

- Ubuntu 22.04 installed
- ROS 2 Humble Hawksbill installed (see installation guide)
- Basic understanding of Python programming
- Familiarity with Linux command line

## Integration with Other Modules

This module serves as the foundation for all other modules in the book:

- Simulation module: Uses ROS 2 messages to control simulated robots
- Isaac module: Leverages ROS 2 for perception system integration
- VLA module: Uses ROS 2 actions to control robot behavior

Understanding ROS 2 communication patterns is crucial for implementing the capstone project where voice commands are transformed into robot actions.