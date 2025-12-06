---
sidebar_position: 5
---

# ROS 2 Examples and Practical Applications

## Overview

This chapter provides practical examples of ROS 2 concepts applied to humanoid robotics. We'll implement the publisher/subscriber pair, create a humanoid URDF model, visualize it in RViz, and send commands from a Python AI agent as mentioned in the User Story 1 acceptance criteria.

This chapter covers:
- Implementing the ROS 2 publisher/subscriber pattern
- Creating a complete humanoid URDF model
- Visualizing the robot in RViz
- Creating a Python AI agent that sends commands to the robot

## Publisher/Subscriber Example

Building on the concepts from the previous chapter, let's implement a complete publisher/subscriber example for a humanoid robot.

### Publisher Node

Create a publisher that sends joint position commands:

```python
# joint_command_publisher.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__('joint_command_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_commands', 10)
        
        # Timer to publish messages at regular intervals
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
        # Define joint names for our humanoid model
        self.joint_names = [
            'left_hip_joint', 'left_knee_joint', 'left_ankle_joint',
            'right_hip_joint', 'right_knee_joint', 'right_ankle_joint',
            'left_shoulder_joint', 'left_elbow_joint',
            'right_shoulder_joint', 'right_elbow_joint'
        ]
        
        self.get_logger().info('Joint Command Publisher initialized')

    def timer_callback(self):
        msg = JointState()
        msg.name = self.joint_names
        msg.position = []
        
        # Generate sinusoidal trajectories for demonstration
        for i, joint in enumerate(self.joint_names):
            # Each joint follows a different sinusoidal pattern
            position = 0.5 * math.sin(self.i * 0.05 + i * 0.2)
            msg.position.append(position)
        
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published joint commands: {msg.position}')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    joint_command_publisher = JointCommandPublisher()
    
    try:
        rclpy.spin(joint_command_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        joint_command_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Node

Create a subscriber that receives joint states and logs them:

```python
# joint_state_subscriber.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            'joint_commands',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Received joint states:')
        for name, position in zip(msg.name, msg.position):
            self.get_logger().info(f'  {name}: {position:.3f}')

def main(args=None):
    rclpy.init(args=args)
    joint_state_subscriber = JointStateSubscriber()
    
    try:
        rclpy.spin(joint_state_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        joint_state_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Complete Humanoid URDF Model

Here's a complete humanoid URDF model using XACRO:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="simple_humanoid">
  <!-- Constants -->
  <xacro:property name="M_PI" value="3.1415926535897931"/>
  <xacro:property name="torso_height" value="0.6"/>
  <xacro:property name="torso_width" value="0.25"/>
  <xacro:property name="torso_depth" value="0.15"/>
  <xacro:property name="head_radius" value="0.12"/>
  <xacro:property name="upper_arm_length" value="0.4"/>
  <xacro:property name="lower_arm_length" value="0.35"/>
  <xacro:property name="upper_leg_length" value="0.5"/>
  <xacro:property name="lower_leg_length" value="0.45"/>
  <xacro:property name="foot_length" value="0.25"/>
  <xacro:property name="foot_width" value="0.12"/>
  <xacro:property name="foot_height" value="0.08"/>

  <!-- Materials -->
  <material name="black">
    <color rgba="0.0 0.0 0.0 1.0"/>
  </material>
  <material name="blue">
    <color rgba="0.0 0.0 0.8 1.0"/>
  </material>
  <material name="green">
    <color rgba="0.0 0.8 0.0 1.0"/>
  </material>
  <material name="grey">
    <color rgba="0.5 0.5 0.5 1.0"/>
  </material>
  <material name="orange">
    <color rgba="1.0 0.423529411765 0.0392156862745 1.0"/>
  </material>
  <material name="brown">
    <color rgba="0.870588235294 0.811764705882 0.764705882353 1.0"/>
  </material>
  <material name="red">
    <color rgba="0.8 0.0 0.0 1.0"/>
  </material>
  <material name="white">
    <color rgba="1.0 1.0 1.0 1.0"/>
  </material>

  <!-- Base origin link -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.01 0.01 0.01"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.01 0.01 0.01"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.001"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 ${torso_height/2}"/>
  </joint>

  <link name="torso">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="${torso_width} ${torso_depth} ${torso_height}"/>
      </geometry>
      <material name="orange"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="${torso_width} ${torso_depth} ${torso_height}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="torso_to_head" type="fixed">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 ${torso_height/2 + head_radius}"/>
  </joint>

  <link name="head">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="${head_radius}"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="${head_radius}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>

  <!-- Neck joint -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="neck"/>
    <origin xyz="0 0 ${torso_height/2}"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="neck">
    <visual>
      <origin xyz="0 0 ${head_radius/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${head_radius}" radius="0.02"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${head_radius/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${head_radius}" radius="0.02"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Left Arm -->
  <joint name="left_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="${torso_width/2} 0 ${torso_height*0.2}" rpy="0 ${M_PI/2} 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="left_upper_arm">
    <visual>
      <origin xyz="0 0 ${-upper_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_arm_length}" radius="0.05"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-upper_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_arm_length}" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 ${-upper_arm_length}"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <origin xyz="0 0 ${-lower_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_arm_length}" radius="0.04"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-lower_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_arm_length}" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>

  <!-- Right Arm -->
  <joint name="right_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="${-torso_width/2} 0 ${torso_height*0.2}" rpy="0 ${-M_PI/2} 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="right_upper_arm">
    <visual>
      <origin xyz="0 0 ${-upper_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_arm_length}" radius="0.05"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-upper_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_arm_length}" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <joint name="right_elbow_joint" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_lower_arm"/>
    <origin xyz="0 0 ${-upper_arm_length}"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="right_lower_arm">
    <visual>
      <origin xyz="0 0 ${-lower_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_arm_length}" radius="0.04"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-lower_arm_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_arm_length}" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>

  <!-- Left Leg -->
  <joint name="left_hip_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_leg"/>
    <origin xyz="${torso_width*0.3} 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/4}" upper="${M_PI/4}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="left_upper_leg">
    <visual>
      <origin xyz="0 0 ${-upper_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_leg_length}" radius="0.06"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-upper_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_leg_length}" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_upper_leg"/>
    <child link="left_lower_leg"/>
    <origin xyz="0 0 ${-upper_leg_length}"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="left_lower_leg">
    <visual>
      <origin xyz="0 0 ${-lower_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_leg_length}" radius="0.05"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-lower_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_leg_length}" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.5"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <joint name="left_ankle_joint" type="revolute">
    <parent link="left_lower_leg"/>
    <child link="left_foot"/>
    <origin xyz="0 0 ${-lower_leg_length}"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/4}" upper="${M_PI/4}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="left_foot">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_length} ${foot_width} ${foot_height}"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_length} ${foot_width} ${foot_height}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Right Leg -->
  <joint name="right_hip_joint" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_leg"/>
    <origin xyz="${-torso_width*0.3} 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/4}" upper="${M_PI/4}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="right_upper_leg">
    <visual>
      <origin xyz="0 0 ${-upper_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_leg_length}" radius="0.06"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-upper_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${upper_leg_length}" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <joint name="right_knee_joint" type="revolute">
    <parent link="right_upper_leg"/>
    <child link="right_lower_leg"/>
    <origin xyz="0 0 ${-upper_leg_length}"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="right_lower_leg">
    <visual>
      <origin xyz="0 0 ${-lower_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_leg_length}" radius="0.05"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 ${-lower_leg_length/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder length="${lower_leg_length}" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.5"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <joint name="right_ankle_joint" type="revolute">
    <parent link="right_lower_leg"/>
    <child link="right_foot"/>
    <origin xyz="0 0 ${-lower_leg_length}"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/4}" upper="${M_PI/4}" effort="100.0" velocity="1.0"/>
  </joint>

  <link name="right_foot">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_length} ${foot_width} ${foot_height}"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_length} ${foot_width} ${foot_height}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Joint State Publisher for visualization -->
  <joint_state_publisher>
    <update_rate>10</update_rate>
  </joint_state_publisher>

  <!-- Robot State Publisher -->
  <robot_state_publisher>
    <update_rate>10</update_rate>
  </robot_state_publisher>
</robot>
```

## Visualization in RViz

To visualize the robot in RViz:

1. Save the XACRO model as `simple_humanoid.urdf.xacro` in your package

2. Create a launch file to start the robot state publisher along with the joint publisher:

```python
# launch_humanoid.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        # Joint command publisher
        Node(
            package='your_package_name',
            executable='joint_command_publisher',
            name='joint_command_publisher',
            output='screen'
        ),
        
        # Robot state publisher (loads and publishes the robot model)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {'use_sim_time': False},
                {'robot_description': 
                 PathJoinSubstitution([
                     FindPackageShare('your_package_name'),
                     'urdf',
                     'simple_humanoid.urdf.xacro'
                 ])}
            ]
        ),
        
        # Joint state publisher (publishes joint states for visualization)
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[
                {'use_sim_time': False},
                {'rate': 10}
            ]
        )
    ])
```

3. To run the visualization:
```bash
# Convert XACRO to URDF (for viewing purposes)
xacro simple_humanoid.urdf.xacro -o simple_humanoid.urdf

# Launch the robot
ros2 launch your_package launch_humanoid.launch.py

# In another terminal, launch RViz
rviz2
```

4. In RViz:
   - Set Fixed Frame to 'base_link'
   - Add RobotModel display
   - Set Robot Description to 'robot_description'

## Python AI Agent Example

Now let's create a Python AI agent that sends commands to our robot model:

```python
# ai_robot_controller.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import time
import math
import threading
import queue

class AIRobotController(Node):
    def __init__(self):
        super().__init__('ai_robot_controller')
        
        # Publisher for joint commands
        self.joint_publisher = self.create_publisher(JointState, 'joint_commands', 10)
        
        # Publisher for status updates
        self.status_publisher = self.create_publisher(String, 'ai_status', 10)
        
        # Define humanoid joint names
        self.joint_names = [
            'left_hip_joint', 'left_knee_joint', 'left_ankle_joint',
            'right_hip_joint', 'right_knee_joint', 'right_ankle_joint',
            'left_shoulder_joint', 'left_elbow_joint',
            'right_shoulder_joint', 'right_elbow_joint'
        ]
        
        # Command queue for thread-safe command handling
        self.command_queue = queue.Queue()
        
        # Timer to process commands at regular intervals
        self.timer = self.create_timer(0.1, self.process_commands)
        
        # Start the AI decision-making process in a separate thread
        self.ai_thread = threading.Thread(target=self.ai_decision_loop)
        self.ai_thread.daemon = True
        self.ai_thread.start()
        
        self.get_logger().info('AI Robot Controller initialized')

    def ai_decision_loop(self):
        """Simulate AI decision-making process"""
        while rclpy.ok():
            try:
                # Get command from queue if available
                command = self.command_queue.get(timeout=1.0)
                
                # Process the command
                if command == "WAVE":
                    self.execute_wave_motion()
                elif command == "WALK":
                    self.execute_walk_motion()
                elif command == "STAND":
                    self.execute_stand_position()
                else:
                    self.get_logger().info(f'Unknown command: {command}')
                    
            except queue.Empty:
                # No commands available, continue loop
                continue

    def execute_wave_motion(self):
        """Execute a waving motion with the right arm"""
        self.get_logger().info('Executing wave motion')
        
        # Wave motion parameters
        wave_duration = 2.0  # seconds
        start_time = self.get_clock().now().nanoseconds * 1e-9
        
        while (self.get_clock().now().nanoseconds * 1e-9 - start_time) < wave_duration:
            current_time = self.get_clock().now().nanoseconds * 1e-9 - start_time
            
            # Create wave motion for right shoulder and elbow
            right_shoulder_pos = 0.5 * math.sin(current_time * 2 * math.pi / 1.0)
            right_elbow_pos = 0.5 * math.cos(current_time * 2 * math.pi / 1.0)
            
            # Publish joint positions
            msg = JointState()
            msg.name = self.joint_names
            msg.position = [0.0] * len(self.joint_names)
            msg.position[self.joint_names.index('right_shoulder_joint')] = right_shoulder_pos
            msg.position[self.joint_names.index('right_elbow_joint')] = right_elbow_pos
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'base_link'
            
            self.joint_publisher.publish(msg)
            
            # Small delay to control update rate
            time.sleep(0.05)
        
        self.get_logger().info('Wave motion completed')

    def execute_walk_motion(self):
        """Execute a simple walking motion pattern"""
        self.get_logger().info('Executing walk motion')
        
        # Walk motion parameters
        walk_duration = 4.0  # seconds
        step_period = 1.0    # seconds per step
        start_time = self.get_clock().now().nanoseconds * 1e-9
        
        while (self.get_clock().now().nanoseconds * 1e-9 - start_time) < walk_duration:
            current_time = self.get_clock().now().nanoseconds * 1e-9 - start_time
            phase = (current_time / step_period) % 2.0
            
            # Calculate joint positions based on phase
            left_hip = 0.2 * math.sin(current_time * 2 * math.pi / step_period)
            right_hip = 0.2 * math.sin(current_time * 2 * math.pi / step_period + math.pi)
            left_knee = abs(0.3 * math.sin(current_time * 2 * math.pi / step_period))
            right_knee = abs(0.3 * math.sin(current_time * 2 * math.pi / step_period + math.pi))
            
            # Publish joint positions
            msg = JointState()
            msg.name = self.joint_names
            msg.position = [0.0] * len(self.joint_names)
            msg.position[self.joint_names.index('left_hip_joint')] = left_hip
            msg.position[self.joint_names.index('right_hip_joint')] = right_hip
            msg.position[self.joint_names.index('left_knee_joint')] = left_knee
            msg.position[self.joint_names.index('right_knee_joint')] = right_knee
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'base_link'
            
            self.joint_publisher.publish(msg)
            
            # Small delay to control update rate
            time.sleep(0.05)
        
        self.get_logger().info('Walk motion completed')

    def execute_stand_position(self):
        """Return to neutral standing position"""
        self.get_logger().info('Executing stand position')
        
        msg = JointState()
        msg.name = self.joint_names
        msg.position = [0.0] * len(self.joint_names)  # All joints to neutral position
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        self.joint_publisher.publish(msg)
        self.get_logger().info('Stand position executed')

    def process_commands(self):
        """Timer callback to publish status messages"""
        status_msg = String()
        status_msg.data = "AI Controller operational"
        self.status_publisher.publish(status_msg)

    def send_command(self, command):
        """Add a command to the processing queue"""
        self.command_queue.put(command)
        self.get_logger().info(f'Command queued: {command}')

def main(args=None):
    rclpy.init(args=args)
    ai_controller = AIRobotController()
    
    # Example: send commands to the robot
    def send_demo_commands():
        time.sleep(2)  # Wait a bit before starting
        ai_controller.send_command("WAVE")
        time.sleep(5)  # Wait for wave to complete
        ai_controller.send_command("WALK")
        time.sleep(8)  # Wait for walk to complete
        ai_controller.send_command("STAND")
    
    # Start the demo commands in a background thread
    demo_thread = threading.Thread(target=send_demo_commands)
    demo_thread.start()
    
    try:
        rclpy.spin(ai_controller)
    except KeyboardInterrupt:
        pass
    finally:
        ai_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Running the Complete Example

To run the complete example:

1. Create a ROS 2 package:
```bash
mkdir -p ~/ros2_ws/src/physical_ai_examples
cd ~/ros2_ws/src/physical_ai_examples
ros2 pkg create --build-type ament_python ai_robot_examples
cd ai_robot_examples
```

2. Create the required files:
   - Copy the Python nodes to `ai_robot_examples/ai_robot_examples/`
   - Create the URDF in `ai_robot_examples/urdf/`
   - Create the launch file in `ai_robot_examples/launch/`

3. Setup the package:
```bash
# Add the required dependencies to package.xml
<depend>rclpy</depend>
<depend>std_msgs</depend>
<depend>sensor_msgs</depend>
<depend>geometry_msgs</depend>
<depend>launch</depend>
<depend>launch_ros</depend>
<depend>robot_state_publisher</depend>
<depend>joint_state_publisher</depend>
```

4. Build and run:
```bash
cd ~/ros2_ws
colcon build --packages-select ai_robot_examples
source install/setup.bash

# Run the AI controller
ros2 run ai_robot_examples ai_robot_controller

# In another terminal, run RViz to visualize
rviz2
```

## Exercises

### Exercise 1: Extend the Humanoid Model
Add fingers to the humanoid model. Each hand should have 5 digits with appropriate joints.

### Exercise 2: Implement More AI Behaviors
Extend the AI controller to implement additional behaviors like sitting, pointing, or dancing.

### Exercise 3: Add Sensors to the Model
Add a camera sensor to the head of the humanoid model and configure it properly in the URDF.

## Summary

In this chapter, we've implemented a complete ROS 2 publisher/subscriber pair, created a humanoid URDF model, visualized it in RViz, and created a Python AI agent that sends commands to the robot. This completes the requirements for User Story 1:

- ✅ Student can create a working ROS 2 publisher/subscriber pair
- ✅ Student can create a humanoid URDF with joints
- ✅ Student can visualize the robot in RViz
- ✅ Student can send commands from a Python AI agent

This foundation provides the necessary groundwork for the subsequent modules on simulation, NVIDIA Isaac, and VLA systems. The integration patterns established here will be essential when connecting these different components in the capstone project.