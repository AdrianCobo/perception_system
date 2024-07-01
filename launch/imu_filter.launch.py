import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    imu_filter_node = Node(package='imu_filter_madgwick', executable='imu_filter_madgwick_node', output='screen',
                      parameters=[{'use_mag': False}], remappings=[('/imu/data_raw', '/camera/camera/imu')])
    delayed_imu_filter_node = TimerAction(period=3.0, actions=[imu_filter_node])

    return LaunchDescription([
        delayed_imu_filter_node
    ])
