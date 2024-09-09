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
        launch_arguments={'use_sim_time': 'false',
                          'enable_accel': 'true',
                          'enable_gyro': 'true',
                          'pointcloud.enable': 'true',
                          'enable_color': 'true'}.items()
    )

    return LaunchDescription([
        camera_with_imu_enabled_node
    ])
