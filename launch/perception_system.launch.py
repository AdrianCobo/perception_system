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
    
    lidar_node = Node(namespace='rslidar_sdk', package='rslidar_sdk', executable='rslidar_sdk_node', output='screen')

    camera_with_imu_enabled_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')]),
        launch_arguments={'enable_accel': 'True', 'enable_gyro': 'True', 'unite_imu_method': '1'}.items()
    )
	
    # constant dt must be equal as scan_period param at lidarslam_ros2 
    imu_filter_node = Node(package='imu_filter_madgwick', executable='imu_filter_madgwick_node', output='screen',
                      parameters=[{'use_mag': False, 'publish_tf': False, 'constant_dt': 0.2 }], remappings=[('/imu/data_raw', '/camera/camera/imu')])

    rviz_config=get_package_share_directory('perception_system')+'/rviz/perception_rviz_config.rviz'
    rviz_node = Node(namespace='rviz2', package='rviz2', executable='rviz2', arguments=['-d',rviz_config])

    return LaunchDescription([
        spawn_system,
        lidar_node,
        camera_with_imu_enabled_node,
        imu_filter_node,
        rviz_node
    ])
