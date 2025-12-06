#!/usr/bin/env python3

"""
AI Robot Controller

This node simulates an AI agent that sends commands to control a humanoid robot.
It demonstrates how AI agents can interact with ROS 2 systems.
"""

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