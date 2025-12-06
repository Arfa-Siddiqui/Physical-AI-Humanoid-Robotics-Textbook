# Quickstart Guide: Physical AI & Humanoid Robotics Book

## Prerequisites

Before starting to contribute to or use this book, ensure you have the following installed:

- **Git** (v2.30 or higher)
- **Node.js** (v18 or higher) and npm (v8 or higher)
- **Ubuntu 22.04** (or equivalent Linux environment)
- **ROS 2 Humble Hawksbill** (or Iron Irwini)
- **Python 3.10+**
- **Basic knowledge of Markdown and Git workflows**

## Setup Docusaurus Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the local development server**:
   ```bash
   npm start
   ```
   This command starts a local development server and opens a browser window with the documentation. Most changes are reflected live without restarting the server.

## Setup ROS 2 Environment

1. **Install ROS 2 Humble Hawksbill** (following official installation guide):
   ```bash
   # Setup locale
   sudo locale-gen en_US.UTF-8
   sudo update-locale LANG=en_US.UTF-8

   # Setup sources
   sudo apt update && sudo apt install -y curl gnupg lsb-release
   curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

   # Install ROS 2 packages
   sudo apt update
   sudo apt install ros-humble-desktop
   sudo apt install ros-dev-tools
   ```

2. **Source the ROS 2 environment**:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

## Creating New Content

1. **Create a new branch for your work**:
   ```bash
   git checkout -b feature/your-topic-name
   ```

2. **Add your content to the appropriate directory**:
   - For ROS 2 content: `docs/modules/ros2/`
   - For Simulation content: `docs/modules/simulation/`
   - For Isaac content: `docs/modules/isaac/`
   - For VLA content: `docs/modules/vla/`
   - For capstone project: `docs/capstone/`

3. **Example new chapter file**:
   ```markdown
   ---
   title: Understanding ROS 2 Nodes
   sidebar_position: 2
   ---

   # Understanding ROS 2 Nodes

   ## What is a ROS 2 Node?

   A ROS 2 node is... [your content here]

   ## Creating Your First Node

   ```python
   import rclpy
   from rclpy.node import Node

   class MinimalPublisher(Node):
       def __init__(self):
           super().__init__('minimal_publisher')
           # Your code here
   ```

   ## Summary

   In this chapter, you learned...
   ```

## Validating Code Examples

1. **Test your ROS 2 code in a simulation environment first**:
   ```bash
   # Create a new ROS 2 workspace
   mkdir -p ~/ros2_book_ws/src
   cd ~/ros2_book_ws

   # Build your packages
   colcon build --packages-select your_package_name

   # Source the workspace
   source install/setup.bash

   # Run your node
   ros2 run your_package_name your_node_name
   ```

2. **Ensure all external links and references are valid**:
   - Check all URLs in your content
   - Verify all citations point to valid resources
   - Test all commands in your code examples

## Building and Previewing

1. **Build the documentation**:
   ```bash
   npm run build
   ```

2. **Serve the built documentation locally**:
   ```bash
   npm run serve
   ```

3. **Check for broken links**:
   ```bash
   npm run lint:links
   ```

## Adding Citations

When adding citations, follow APA style format. Here's an example:

```markdown
According to Smith et al. (2023), the use of simulation environments is crucial for developing safe robotics applications [1].

References:

[1] Smith, J., Johnson, A., & Williams, B. (2023). Safe robotics development using simulation. Journal of Robotics, 15(3), 45-67. https://doi.org/10.1234/example
```

## Contributing Workflow

1. **Create an issue** for the content you're planning to add (if one doesn't exist)

2. **Fork the repository** and create a feature branch

3. **Write your content** following the project's style guide

4. **Add proper citations** for all technical claims

5. **Validate code examples** by testing them in your environment

6. **Update the table of contents** if you're adding new sections

7. **Submit a pull request** with your changes

8. **Wait for review and address feedback** as needed

## Style Guidelines

- Use second-person narrative ("you can do this..." instead of "one can do this...")
- Write at Flesch-Kincaid grade level 10-12
- Include practical examples with real code
- Provide clear learning objectives for each section
- Use consistent terminology throughout the book

## Troubleshooting

**Problem**: Docusaurus fails to start
- Solution: Ensure all dependencies are installed (`npm install`) and check Node.js version

**Problem**: ROS 2 commands not found
- Solution: Ensure ROS 2 environment is sourced (`source /opt/ros/humble/setup.bash`)

**Problem**: Build fails with Markdown errors
- Solution: Check for syntax errors in your Markdown files and ensure proper formatting

For more help, check the full documentation in the `docs/` folder or create an issue in the repository.