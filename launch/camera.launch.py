import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    camera_config_yaml=get_package_share_directory('perception_system')+'/config/camera_config.yaml'
    camera_config_json=get_package_share_directory('perception_system')+'/config/camera_config.json'

    camera_with_imu_enabled_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')]),
        launch_arguments={'config_file': camera_config_yaml, 'json_file_path': camera_config_json}.items()
    )

    return LaunchDescription([
        camera_with_imu_enabled_node
    ])
