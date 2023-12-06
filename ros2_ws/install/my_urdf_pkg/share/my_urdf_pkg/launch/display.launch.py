#!/usr/bin/env python3
import os
import sys
from ament_index_python.packages import get_package_share_directory
import launch
import launch_ros.actions

def generate_launch_description():
    # Load the URDF into a parameter
    bringup_dir = '/home/bravenderbros/ros2_ws/src/my_urdf_pkg/urdf/'
    urdf_path = os.path.join(bringup_dir, 'my_robot.urdf')
    urdf = open(urdf_path).read()

    return launch.LaunchDescription([
        launch_ros.actions.Node(
            name='robot_state_publisher',
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': urdf}],
        ),
        #launch_ros.actions.Node(
         #   name='joint_state_publisher',
         #   package='joint_state_publisher_gui',
         #   executable='joint_state_publisher_gui'
        # ),

        launch_ros.actions.Node(
            name='rviz',
            package='rviz2',
            executable='rviz2'
        ),
    ])

def main(argv=sys.argv[1:]):
    ld = generate_launch_description()
    ls = launch.LaunchService(argv=argv)
    ls.include_launch_description(ld)
    return ls.run()

if __name__ == '__main__':
    main()