# Content API Specification

This document outlines the API contracts for the Physical AI & Humanoid Robotics Book content management system.

## Base URL
`https://physical-ai-book.example.com/api/v1`

## Content Endpoints

### Get All Modules
- **Endpoint**: `GET /modules`
- **Description**: Retrieve a list of all available modules in the book
- **Parameters**: None
- **Response**:
  ```json
  {
    "modules": [
      {
        "id": "ros2-fundamentals",
        "title": "ROS 2 Fundamentals",
        "description": "Introduction to ROS 2 concepts, nodes, topics, and services",
        "priority": "P1",
        "estimatedHours": 10,
        "learningObjectives": [
          "Understand ROS 2 architecture",
          "Create ROS 2 nodes and publishers",
          "Implement communication patterns"
        ]
      },
      {
        "id": "simulation",
        "title": "Simulation Environments",
        "description": "Creating digital twins with Gazebo and Unity",
        "priority": "P2",
        "estimatedHours": 8,
        "learningObjectives": [
          "Set up simulation environments",
          "Create robot models for simulation",
          "Test control algorithms in simulation"
        ]
      }
    ]
  }
  ```

### Get Module Details
- **Endpoint**: `GET /modules/{moduleId}`
- **Description**: Retrieve detailed information about a specific module
- **Parameters**:
  - `moduleId` (path): The unique identifier for the module
- **Response**:
  ```json
  {
    "id": "ros2-fundamentals",
    "title": "ROS 2 Fundamentals",
    "description": "Introduction to ROS 2 concepts, nodes, topics, and services",
    "priority": "P1",
    "estimatedHours": 10,
    "learningObjectives": [
      "Understand ROS 2 architecture",
      "Create ROS 2 nodes and publishers",
      "Implement communication patterns"
    ],
    "chapters": [
      {
        "id": "ros2-intro",
        "title": "Introduction to ROS 2",
        "position": 1,
        "learningObjectives": [
          "Understand ROS 2 architecture",
          "Explain the differences between ROS 1 and ROS 2"
        ]
      },
      {
        "id": "ros2-nodes",
        "title": "ROS 2 Nodes and Communication",
        "position": 2,
        "learningObjectives": [
          "Create ROS 2 nodes",
          "Implement publishers and subscribers"
        ]
      }
    ],
    "prerequisites": []
  }
  ```

### Get Chapter Content
- **Endpoint**: `GET /modules/{moduleId}/chapters/{chapterId}`
- **Description**: Retrieve the content of a specific chapter
- **Parameters**:
  - `moduleId` (path): The unique identifier for the module
  - `chapterId` (path): The unique identifier for the chapter
- **Response**:
  ```json
  {
    "id": "ros2-nodes",
    "moduleId": "ros2-fundamentals",
    "title": "ROS 2 Nodes and Communication",
    "position": 2,
    "learningObjectives": [
      "Create ROS 2 nodes",
      "Implement publishers and subscribers"
    ],
    "content": "# ROS 2 Nodes and Communication\n\nIn this chapter, we'll explore...",
    "contentBlocks": [
      {
        "id": "block-1",
        "type": "text",
        "content": "A ROS 2 node is the fundamental unit of computation...",
        "position": 1
      },
      {
        "id": "block-2",
        "type": "code",
        "content": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalPublisher(Node):\n    def __init__(self):\n        super().__init__('minimal_publisher')",
        "position": 2
      },
      {
        "id": "block-3",
        "type": "exercise",
        "content": "Create a subscriber node that receives messages from the publisher",
        "difficulty": "intermediate",
        "position": 3
      }
    ],
    "citations": [
      {
        "id": "ros2-concepts-2023",
        "title": "ROS 2 Concepts",
        "authors": ["Open Robotics"],
        "url": "https://docs.ros.org/en/humble/Concepts.html",
        "type": "documentation"
      }
    ]
  }
  ```

### Search Content
- **Endpoint**: `GET /search`
- **Description**: Search across all book content
- **Parameters**:
  - `q` (query): Search query string
  - `limit` (query, optional): Maximum number of results (default: 10)
  - `offset` (query, optional): Number of results to skip (default: 0)
- **Response**:
  ```json
  {
    "query": "ROS 2 nodes",
    "totalResults": 5,
    "results": [
      {
        "id": "ros2-nodes",
        "title": "ROS 2 Nodes and Communication",
        "module": "ROS 2 Fundamentals",
        "type": "chapter",
        "preview": "A ROS 2 node is the fundamental unit of computation in ROS 2...",
        "url": "/modules/ros2-fundamentals/chapters/ros2-nodes"
      },
      {
        "id": "block-2",
        "title": "Code Example: Minimal Publisher",
        "module": "ROS 2 Fundamentals",
        "chapter": "ROS 2 Nodes and Communication",
        "type": "content-block",
        "preview": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalPublisher(Node):...",
        "url": "/modules/ros2-fundamentals/chapters/ros2-nodes#block-2"
      }
    ]
  }
  ```

## Citation Endpoints

### Get All Citations
- **Endpoint**: `GET /citations`
- **Description**: Retrieve all citations used in the book
- **Parameters**:
  - `type` (query, optional): Filter by citation type (academic-paper, documentation, book, web-resource)
  - `peerReviewed` (query, optional): Filter by peer review status (true/false)
- **Response**:
  ```json
  {
    "citations": [
      {
        "id": "ros2-concepts-2023",
        "type": "documentation",
        "title": "ROS 2 Concepts",
        "authors": ["Open Robotics"],
        "publicationDate": "2023-01-01",
        "url": "https://docs.ros.org/en/humble/Concepts.html",
        "isPeerReviewed": false
      },
      {
        "id": "isaac-sim-2023",
        "type": "documentation",
        "title": "NVIDIA Isaac Sim Documentation",
        "authors": ["NVIDIA"],
        "publicationDate": "2023-05-15",
        "url": "https://docs.nvidia.com/isaac-sim/",
        "isPeerReviewed": false
      }
    ]
  }
  }
  ```

## Validation Endpoints

### Validate Code Example
- **Endpoint**: `POST /validate-code`
- **Description**: Validate a code example against specified requirements
- **Request Body**:
  ```json
  {
    "code": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalPublisher(Node):\n    def __init__(self):\n        super().__init__('minimal_publisher')",
    "language": "python",
    "requirements": ["ros2-humble"]
  }
  ```
- **Response**:
  ```json
  {
    "isValid": true,
    "language": "python",
    "syntaxErrors": [],
    "dependencyIssues": [],
    "validationNotes": "Code appears valid for ROS 2 Humble"
  }
  ```