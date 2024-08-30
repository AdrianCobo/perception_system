import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():



    camera_with_imu_enabled_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')]),
        launch_arguments={'config_file': '/home/adrianco/Desktop/ros2_ws/install/perception_system/share/perception_system/config/camera_config.yaml'}.items()
    )

    return LaunchDescription([
        camera_with_imu_enabled_node,
    ])
