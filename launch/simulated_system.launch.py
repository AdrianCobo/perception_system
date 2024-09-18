import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    spawn_system = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('perception_system'), 'launch', 'spawn_systems.launch.py')]))
	
    # constant dt must be equal as scan_period param at lidarslam_ros2 
    imu_filter_node = Node(package='imu_filter_madgwick', executable='imu_filter_madgwick_node', output='screen',
                      parameters=[{'use_mag': False, 'publish_tf': False, 'constant_dt': 0.2 }], remappings=[('/imu/data_raw', '/camera/camera/imu')])

    return LaunchDescription([
        spawn_system,
        imu_filter_node,
    ])
