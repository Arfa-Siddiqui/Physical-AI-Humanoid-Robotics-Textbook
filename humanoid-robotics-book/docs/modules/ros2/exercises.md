---
sidebar_position: 6
---

# ROS 2 Exercises

## Overview

This section contains exercises to reinforce the concepts covered in the ROS 2 fundamentals module. Each exercise builds on the knowledge gained from the previous chapters and helps solidify your understanding of ROS 2 concepts as they apply to humanoid robotics.

## Exercise 1: Basic Publisher/Subscriber

### Objective
Create a simple publisher that publishes "Hello World" messages and a subscriber that receives and logs them.

### Instructions
1. Create a new ROS 2 package called `hello_world_demo`
2. Create a publisher node that publishes a String message containing "Hello World" every 2 seconds
3. Create a subscriber node that receives these messages and logs them to the console
4. Test that both nodes communicate properly

### Starter Code
```python
# publisher_member_function.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Solution
The solution involves creating a subscriber node similar to the publisher. You can refer to the examples in the previous chapter for the subscriber implementation.

### Learning Objectives
- Understand the publisher/subscriber pattern in ROS 2
- Learn how to create ROS 2 nodes in Python
- Practice using ROS 2 messages and topics

## Exercise 2: Service Integration

### Objective
Create a service that controls a simulated joint and a client that calls it.

### Instructions
1. Implement a service server that accepts joint name and target position as parameters
2. Implement a service client that calls the service with different joint configurations
3. Add error handling for invalid joint names or positions

### Starter Code
```python
# joint_control_service.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool

class JointControlService(Node):
    def __init__(self):
        super().__init__('joint_control_service')
        self.srv = self.create_service(
            SetBool, 
            'control_joint', 
            self.control_joint_callback
        )

    def control_joint_callback(self, request, response):
        # TODO: Implement joint control logic
        self.get_logger().info(f'Received request to control joint')
        response.success = True
        response.message = "Joint control request processed"
        return response

def main(args=None):
    rclpy.init(args=args)
    joint_control_service = JointControlService()
    
    try:
        rclpy.spin(joint_control_service)
    except KeyboardInterrupt:
        pass
    finally:
        joint_control_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Learning Objectives
- Understand ROS 2 services and the request/response pattern
- Learn how to create service servers and clients
- Practice error handling in ROS 2

## Exercise 3: Action-Based Movement

### Objective
Implement an action server that moves a joint to a target position with feedback on progress.

### Instructions
1. Create an action interface for joint movement (or use `control_msgs/FollowJointTrajectory`)
2. Implement an action server that simulates joint movement
3. Provide feedback on the progress of the movement
4. Implement an action client that sends goals to the server

### Starter Code
```python
# joint_movement_action_server.py
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
import time

class JointMovementActionServer(Node):
    def __init__(self):
        super().__init__('joint_movement_action_server')
        # TODO: Define your action type
        self._action_server = ActionServer(
            self,
            # Your action type,
            'joint_movement',
            self.execute_callback
        )

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        # TODO: Implement movement logic with feedback
        # Simulate movement process
        for i in range(0, 10):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return  # Your result type()  # Return appropriate result

            # Update feedback
            # feedback_msg = YourAction.Feedback()
            # feedback_msg.progress = float(i) / 10.0
            # goal_handle.publish_feedback(feedback_msg)
            
            time.sleep(0.5)  # Simulate movement time

        goal_handle.succeed()
        # result = YourAction.Result()
        # result.completed = True
        # return result

def main(args=None):
    rclpy.init(args=args)
    joint_movement_action_server = JointMovementActionServer()
    
    try:
        rclpy.spin(joint_movement_action_server)
    except KeyboardInterrupt:
        pass
    finally:
        joint_movement_action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Learning Objectives
- Understand ROS 2 actions for long-running tasks
- Learn how to implement action servers and clients
- Practice providing feedback during long-running operations

## Exercise 4: Humanoid URDF Extension

### Objective
Extend the humanoid model from the examples by adding fingers to the hands.

### Instructions
1. Modify the XACRO file for the humanoid model
2. Add finger links and joints to both hands
3. Each finger should have at least 2 joints (for bending at the knuckles)
4. Ensure the model remains structurally sound and properly connected

### Learning Objectives
- Deepen understanding of URDF and XACRO
- Learn to model complex articulated structures
- Practice maintaining proper joint hierarchies

## Exercise 5: AI Command Enhancement

### Objective
Enhance the AI robot controller to implement additional behaviors.

### Instructions
1. Extend the AI controller from the examples to add a "pointing" behavior
2. The robot should be able to point at specific coordinates in space
3. Implement inverse kinematics logic to position the arm appropriately
4. Add validation to ensure joint limits are not exceeded

### Learning Objectives
- Apply ROS 2 concepts to complex robotic tasks
- Practice integrating perception and action systems
- Learn to validate robot commands against physical constraints

## Exercise 6: Sensor Integration

### Objective
Add a camera sensor to the head of the humanoid model and configure it properly.

### Instructions
1. Add a camera sensor definition in the URDF model
2. Configure the camera properties (resolution, field of view, etc.)
3. Add appropriate plugins for the simulation environment
4. Test the sensor in a simulation environment if available

### Learning Objectives
- Learn to add sensors to robot models
- Understand sensor configuration in URDF
- Practice integrating perception systems with robot models

## Solutions and Hints

Solutions to these exercises are available in the examples directory of the repository. Try to complete the exercises on your own before looking at the solutions.

## Assessment Criteria

Your implementation will be assessed based on:
- Correctness: The code functions as specified
- Code quality: Proper ROS 2 conventions are followed
- Documentation: Code is well-commented and easy to understand
- Testing: Implementation has been tested and validated

## Next Steps

After completing these exercises, you should have a solid understanding of ROS 2 concepts as they apply to humanoid robotics. This knowledge will be essential for the next modules covering simulation, NVIDIA Isaac, and VLA systems.