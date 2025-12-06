---
sidebar_position: 4
---

# URDF and Robot Modeling

## Overview

URDF (Unified Robot Description Format) is an XML format used to describe robot models in ROS. It's essential for humanoid robotics as it defines the physical structure, joints, and properties of the robot. This chapter covers creating humanoid robot models using both URDF and XACRO.

This chapter covers:
- URDF basics and structure
- Defining links and joints for humanoid robots
- Using XACRO to simplify complex models
- Visualizing robots in RViz
- Creating humanoid-specific models

## URDF Basics

URDF is an XML format that describes a robot in terms of links and joints that connect them.

### Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Links define rigid bodies -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Joints connect links -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```

### Links

Links represent rigid bodies in the robot. Each link contains:
- **Visual**: How the link appears in visualizations
- **Collision**: The collision geometry for physics simulation
- **Inertial**: Physical properties like mass and inertia

### Joints

Joints connect links and define their motion. Types include:
- **Fixed**: No movement between links
- **Revolute**: Rotational motion with limits
- **Continuous**: Unlimited rotational motion
- **Prismatic**: Linear sliding motion with limits
- **Planar**: Motion on a plane
- **Floating**: 6DOF motion

## Humanoid Robot URDF

Humanoid robots require more complex models with multiple limbs and joints. Here's a simplified example:

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot">
  <!-- Base of the robot -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.25"/>
  </joint>

  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.3 0.5"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.3 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="torso_to_head" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.35"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.004" ixy="0.0" ixz="0.0" iyy="0.004" iyz="0.0" izz="0.004"/>
    </inertial>
  </link>
</robot>
```

## XACRO: XML Macros

XACRO (XML Macros) is an XML macro language that makes URDF files more readable and maintainable by allowing definitions, properties, and includes.

### Basic XACRO Concepts

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="example_robot">
  <!-- Properties -->
  <xacro:property name="M_PI" value="3.14159"/>
  <xacro:property name="base_width" value="0.3"/>
  <xacro:property name="base_length" value="0.5"/>
  <xacro:property name="base_height" value="0.2"/>

  <!-- Define a macro for creating a wheel -->
  <xacro:macro name="wheel" params="prefix parent xyz">
    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="${parent}"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="${xyz}" rpy="0 ${M_PI/2} 0"/>
      <axis xyz="0 0 1"/>
    </joint>

    <link name="${prefix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="0.1" length="0.05"/>
        </geometry>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="0.1" length="0.05"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="1.0"/>
        <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
      </inertial>
    </link>
  </xacro:macro>

  <!-- Use the macro to create wheels -->
  <xacro:wheel prefix="front_left" parent="base_link" xyz="0.2 0.15 0"/>
  <xacro:wheel prefix="front_right" parent="base_link" xyz="0.2 -0.15 0"/>
</robot>
```

### Math Expressions in XACRO

XACRO supports mathematical expressions:

```xml
<xacro:property name="wheel_radius" value="0.1"/>
<xacro:property name="wheel_width" value="0.05"/>
<xacro:property name="wheel_x_offset" value="${wheel_radius + 0.05}"/>
```

### Conditional Macros

```xml
<xacro:macro name="sensor" params="sensor_type *origin">
  <xacro:if value="${sensor_type == 'camera'}">
    <sensor name="camera">
      <camera>
        <image width="640" height="480" format="R8G8B8"/>
      </camera>
    </sensor>
  </xacro:if>
  
  <xacro:if value="${sensor_type == 'lidar'}">
    <sensor name="lidar">
      <ray>
        <range min="0.1" max="10.0" resolution="0.01"/>
      </ray>
    </sensor>
  </xacro:if>
</xacro:macro>
```

## Humanoid-Specific Considerations

When modeling humanoid robots, consider these specific requirements:

### Anthropometric Data

Humanoid robots should follow human-like proportions:
- Leg length is approximately 45% of total height
- Arm length is approximately 35% of total height
- Head size is approximately 8-9% of total height

### Joint Range of Motion

Humanoid joints have specific ranges of motion:
- Shoulder abduction: ±90°
- Shoulder flexion: -10° to +180°
- Elbow flexion: 0° to +150°
- Hip flexion: -10° to +120°
- Knee flexion: 0° to +135°

### Balance and Stability

For humanoid robots, consider:
- Center of mass location
- Foot size for stability
- Joint stiffness for balance

## Visualizing Robots in RViz

After creating your URDF, visualize it in RViz:

1. Launch the robot state publisher:
```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:=$(cat robot.urdf)
```

2. In another terminal, launch RViz:
```bash
rviz2
```

3. Add a RobotModel display and set the Fixed Frame to 'base_link'

## URDF Tools and Validation

### Checking URDF Files

Use the check_urdf tool to validate your URDF:

```bash
check_urdf robot.urdf
```

### Converting XACRO to URDF

Convert XACRO files to URDF:

```bash
xacro input.xacro -o output.urdf
```

Or in a launch file:
```xml
<param name="robot_description" command="xacro $(find-pkg-share my_package)/urdf/robot.xacro"/>
```

## Common URDF Issues and Solutions

### Mass Issues
- Each link must have a non-zero mass
- Inertia values must be physically plausible

### Joint Issues
- Joint limits must be consistent with physical constraints
- Joint types must match intended motion

### Visualization Issues
- Ensure visual and collision geometries are properly defined
- Check that origin transforms are correct

## Exercise: Simple Humanoid Model

Create a simplified humanoid robot model with:
- Torso
- Head
- Two arms with shoulder and elbow joints
- Two legs with hip and knee joints

Use XACRO to define the components and avoid duplication.

## Best Practices

1. **Start Simple**: Begin with a basic model and add complexity gradually
2. **Use XACRO**: Leverage macros and properties to make models maintainable
3. **Validate Early**: Check your URDF frequently with validation tools
4. **Follow Conventions**: Use consistent naming and structure
5. **Include Materials**: Define colors and materials for better visualization

## Summary

URDF and XACRO are essential for defining humanoid robot models in ROS. Understanding how to create accurate and efficient robot descriptions is crucial for both simulation and real robot control. XACRO's macro system makes it easier to create complex models while avoiding repetition and errors.

In the next section, we'll look at practical examples of ROS 2 code and how to use URDF models in real applications.