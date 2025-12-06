---
sidebar_position: 3
---

# ROS 2 Nodes and Communication

## Overview

In ROS 2, nodes are the fundamental unit of computation that communicate with each other through various communication patterns. Understanding nodes and communication is essential for creating humanoid robot applications.

This chapter covers:
- Creating and managing ROS 2 nodes
- Using topics for asynchronous communication
- Using services for synchronous request/response communication
- Using actions for goal-oriented communication

## What is a Node?

A node is a process that performs computation. Nodes are combined together into a graph and communicate with each other using topics, services, actions, and parameters.

### Creating a Basic Node

Here's a minimal example of a ROS 2 node in Python:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
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

### Node Naming and Lifecycle

Nodes in ROS 2 are identified by unique names. The lifecycle of a node includes:

1. **Initialization**: The node is created and initialized
2. **Activation**: The node becomes active and can participate in communication
3. **Deactivation**: The node stops participating in communication
4. **Cleanup**: Resources are released
5. **Shutdown**: The node is destroyed

## Topics - Asynchronous Communication

Topics allow for asynchronous, one-way communication between nodes using a publish/subscribe pattern.

### Publishers and Subscribers

- **Publisher**: Sends data to a topic
- **Subscriber**: Receives data from a topic

```python
# Publisher example
publisher = node.create_publisher(String, 'topic_name', 10)

# Subscriber example
subscriber = node.create_subscription(
    String,
    'topic_name',
    callback_function,
    10  # queue size
)
```

### Quality of Service (QoS)

QoS settings define how messages are handled in terms of reliability and durability:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

qos_profile = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,  # or RELIABLE
    durability=DurabilityPolicy.VOLATILE     # or TRANSIENT_LOCAL
)
```

## Services - Synchronous Communication

Services provide synchronous request/response communication between nodes.

### Creating a Service Server

```python
from example_interfaces.srv import AddTwoInts

def add_two_ints_callback(request, response):
    response.sum = request.a + request.b
    self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
    return response

service = node.create_service(AddTwoInts, 'add_two_ints', add_two_ints_callback)
```

### Creating a Service Client

```python
client = node.create_client(AddTwoInts, 'add_two_ints')

while not client.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Service not available, waiting again...')

request = AddTwoInts.Request()
request.a = 41
request.b = 1

future = client.call_async(request)
```

## Actions - Goal-Oriented Communication

Actions are used for long-running tasks that provide feedback and can be canceled.

### Creating an Action Server

```python
from example_interfaces.action import Fibonacci
import threading

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]
        
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()
            
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            
            goal_handle.publish_feedback(feedback_msg)
        
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result
```

### Creating an Action Client

```python
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)
        
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.sequence))
```

## Parameters

Parameters are named, typed values that can be used to configure nodes:

```python
# Declare a parameter
param = self.declare_parameter('param_name', 'default_value')

# Get parameter value
param_value = self.get_parameter('param_name').value
```

## Launch Files

Launch files allow you to start multiple nodes with a single command:

```xml
<launch>
  <node pkg="demo_nodes_py" exec="listener" name="listener1"/>
  <node pkg="demo_nodes_py" exec="talker" name="talker1"/>
</launch>
```

Or using Python:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='listener1'
        ),
        Node(
            package='demo_nodes_py',
            executable='talker',
            name='talker1'
        )
    ])
```

## Communication Patterns for Humanoid Robots

When developing humanoid robots, different communication patterns serve specific purposes:

- **Topics**: Sensor data, motor commands, state information
- **Services**: Calibration, configuration changes, immediate responses
- **Actions**: Complex behaviors like walking, grasping, navigation

## Best Practices

1. **Use appropriate QoS settings** based on your application requirements
2. **Follow naming conventions** for topics, services, and parameters
3. **Handle errors gracefully** in callbacks and communication
4. **Use linters** to ensure code quality
5. **Test nodes independently** before integrating them

## Exercises

### Exercise 1: Basic Publisher/Subscriber
Create a simple publisher that publishes "Hello World" messages and a subscriber that receives and logs them.

### Exercise 2: Service Integration
Create a service that controls a simulated joint and a client that calls it.

### Exercise 3: Action-Based Movement
Implement an action server that moves a joint to a target position with feedback on progress.

## Summary

Understanding ROS 2 communication patterns is crucial for developing humanoid robot applications. The choice between topics, services, and actions depends on your specific use case:

- Use topics for continuous data streams
- Use services for immediate request/response interactions
- Use actions for long-running, cancellable tasks with feedback

In the next section, we'll explore URDF and robot modeling, which will help us define the structure of our humanoid robot.