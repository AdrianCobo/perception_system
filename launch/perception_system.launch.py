import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    lidar_node = Node(namespace='rslidar_sdk', package='rslidar_sdk', executable='rslidar_sdk_node', output='screen')

    camera_with_imu_enabled_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')]),
        launch_arguments={'use_sim_time': 'false',
                          'enable_accel': 'true',
                          'enable_gyro': 'true',
                          'unite_imu_method': '1',
                          'pointcloud.enable': 'true'}.items()
    )

    imu_filter_node = Node(package='imu_filter_madgwick', executable='imu_filter_madgwick_node', output='screen',
                      parameters=[{'use_mag': False}], remappings=[('/imu/data_raw', '/camera/camera/imu')])
    
    fake_tf_node = Node(package='tf2_ros', executable='static_transform_publisher', output='screen',
                      arguments = ["0", "0", "0", "0", "0", "0", "odom", "camera_link"])

    fake_tf_node_2 = Node(package='tf2_ros', executable='static_transform_publisher', output='screen',
                      arguments = ["0", "0", "0", "0", "0", "0", "camera_link", "rslidar"])

    rviz_config=get_package_share_directory('perception_system')+'/rviz/perception_rviz_config.rviz'
    rviz_node = Node(namespace='rviz2', package='rviz2', executable='rviz2', arguments=['-d',rviz_config])

    return LaunchDescription([
        lidar_node,
        camera_with_imu_enabled_node,
        fake_tf_node,
        fake_tf_node_2,
        imu_filter_node,
        rviz_node
    ])
