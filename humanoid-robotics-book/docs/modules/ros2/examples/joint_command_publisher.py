#!/usr/bin/env python3

"""
Joint Command Publisher

This node publishes joint position commands to control a humanoid robot.
It demonstrates the publisher/subscriber pattern in ROS 2.
"""

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