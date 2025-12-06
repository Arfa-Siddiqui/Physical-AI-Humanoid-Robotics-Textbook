// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Modules',
      items: [
        {
          type: 'category',
          label: 'ROS 2 Fundamentals',
          items: [
            'modules/ros2/overview',
            'modules/ros2/installation',
            'modules/ros2/nodes',
            'modules/ros2/urdf',
            'modules/ros2/examples',
            'modules/ros2/exercises'
          ],
        },
      ],
    },
  ],
};

module.exports = sidebars;