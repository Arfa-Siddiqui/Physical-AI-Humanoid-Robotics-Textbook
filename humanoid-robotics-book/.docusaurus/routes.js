import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/humanoid-robotics-book/__docusaurus/debug',
    component: ComponentCreator('/humanoid-robotics-book/__docusaurus/debug', 'fbb'),
    exact: true
  },
  {
    path: '/humanoid-robotics-book/__docusaurus/debug/config',
    component: ComponentCreator('/humanoid-robotics-book/__docusaurus/debug/config', '58c'),
    exact: true
  },
  {
    path: '/humanoid-robotics-book/__docusaurus/debug/content',
    component: ComponentCreator('/humanoid-robotics-book/__docusaurus/debug/content', '9ef'),
    exact: true
  },
  {
    path: '/humanoid-robotics-book/__docusaurus/debug/globalData',
    component: ComponentCreator('/humanoid-robotics-book/__docusaurus/debug/globalData', '5e0'),
    exact: true
  },
  {
    path: '/humanoid-robotics-book/__docusaurus/debug/metadata',
    component: ComponentCreator('/humanoid-robotics-book/__docusaurus/debug/metadata', 'a6b'),
    exact: true
  },
  {
    path: '/humanoid-robotics-book/__docusaurus/debug/registry',
    component: ComponentCreator('/humanoid-robotics-book/__docusaurus/debug/registry', '969'),
    exact: true
  },
  {
    path: '/humanoid-robotics-book/__docusaurus/debug/routes',
    component: ComponentCreator('/humanoid-robotics-book/__docusaurus/debug/routes', '919'),
    exact: true
  },
  {
    path: '/humanoid-robotics-book/docs',
    component: ComponentCreator('/humanoid-robotics-book/docs', '65e'),
    routes: [
      {
        path: '/humanoid-robotics-book/docs',
        component: ComponentCreator('/humanoid-robotics-book/docs', '8e5'),
        routes: [
          {
            path: '/humanoid-robotics-book/docs',
            component: ComponentCreator('/humanoid-robotics-book/docs', '424'),
            routes: [
              {
                path: '/humanoid-robotics-book/docs/intro',
                component: ComponentCreator('/humanoid-robotics-book/docs/intro', 'b29'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/humanoid-robotics-book/docs/modules/ros2/examples',
                component: ComponentCreator('/humanoid-robotics-book/docs/modules/ros2/examples', '129'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/humanoid-robotics-book/docs/modules/ros2/exercises',
                component: ComponentCreator('/humanoid-robotics-book/docs/modules/ros2/exercises', 'f47'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/humanoid-robotics-book/docs/modules/ros2/installation',
                component: ComponentCreator('/humanoid-robotics-book/docs/modules/ros2/installation', '361'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/humanoid-robotics-book/docs/modules/ros2/nodes',
                component: ComponentCreator('/humanoid-robotics-book/docs/modules/ros2/nodes', 'ce3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/humanoid-robotics-book/docs/modules/ros2/overview',
                component: ComponentCreator('/humanoid-robotics-book/docs/modules/ros2/overview', '356'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/humanoid-robotics-book/docs/modules/ros2/urdf',
                component: ComponentCreator('/humanoid-robotics-book/docs/modules/ros2/urdf', '5f0'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
