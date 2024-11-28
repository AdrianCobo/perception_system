# perception_system


## Set Up
1) Instala Ros 2 [Jazzy](https://docs.ros.org/en/jazzy/Installation.html) o [Humble](https://docs.ros.org/en/humble/Installation.html)
2) Instala Cyclone como rmw_dds (opcional)
```shell
sudo apt install ros-$ROS_DISTRO-rmw-cyclonedds-cpp*
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```
3) Sigue las instrucciones de instalación del paquete de ROS2 para el LiDAR [RS-Helios](https://github.com/AdrianCobo/rslidar_sdk) y de [lidar_slam](https://github.com/rsasaki0109/lidarslam_ros2)  
**Para que lidar_slam compile en ubuntu 24 es necesario instalar también**: 
```shell
sudo apt install libg2o-dev
```

**Si quieres instalar MOLA también ejecuta**:
```shell
sudo apt install ros-$ROS_DISTRO-mola ros-$ROS_DISTRO-mola-lidar-odometry
```

4) Clona este [repositorio](https://github.com/AdrianCobo/perception_system.git) en tu directorio ~your_ros2_ws/src.
```shell
cd ~your_ros2_ws/src
git clone https://github.com/AdrianCobo/perception_system.git
```


5) Asegurate de tener instalado todos los paquetes necesarios:
```shell
sudo apt install ros-$ROS_DISTRO-librealsense2-* ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-realsense2-description ros-$ROS_DISTRO-imu-filter-madgwick-* ros-$ROS_DISTRO-realsense2-*
rosdep update
rosdep install --from-paths src
```

5) Compila
```shell
cd ~your_ros2_ws
colcon build --symlink-install --packages-select perception_system
source ./install/setup.bash
```

## Contrucción de mapa 3D con lidar_slam:
```shell
ros2 launch perception_system perception_system.launch.py
ros2 launch perception_system lidarslam.launch.py
```
**Si quieres usar la imu necesitas realizar los siguientes cambios**:  
- En ~your_ros2_ws/src/perception_systemconfig/lidarslam.yaml cambia el parámetro 'use_imu' a True y el parámetro 'scan_period' al (numero de mensajes publicados por tu IMU)/segundos (0.005 en el caso de los rosbags).

## Contrucción de mapa 3D con MOLA:
```shell
ros2 launch perception_system perception_system.launch.py
ros2 launch mola_lidar_odometry ros2-lidar-odometry.launch.py lidar_topic_name:=/rslidar_points
```


## Simulación el sistema con lidar_slam:
```shell
ros2 launch perception_system simulated_system.launch.py
ros2 launch perception_system lidarslam.launch.py
ros2 bag play $(rosbag_selected)
```
**Si quieres usar la imu necesitas realizar los siguientes cambios**:  
- En ~your_ros2_ws/src/perception_systemconfig/lidarslam.yaml cambia el parámetro 'use_imu' a True y el parámetro 'scan_period' al (numero de mensajes publicados por tu IMU)/segundos (0.005 en el caso de los rosbags).

## Simulación el sistema con mola:
```shell
ros2 launch perception_system simulated_system.launch.py
ros2 launch mola_lidar_odometry ros2-lidar-odometry.launch.py lidar_topic_name:=/rslidar_points
ros2 bag play $(rosbag_selected)
```

## Resultado de usar el sistema de percepción con lidar_slam
[![Resultado del Experimento](https://moresales.ca/wp-content/uploads/2022/06/Click-Me-2.png)](https://drive.google.com/file/d/1VGTcvLKiD8vrUgkvgi9_q75DOobXr2hW/view?usp=sharing)
 
## Componentes empleados:
Procesador:
- [Jetson AGX Xavier](https://www.nvidia.com/es-la/autonomous-machines/embedded-systems/jetson-agx-xavier/)
- [Intel® NUC NUC5i5RYK](https://www.intel.la/content/www/xl/es/products/sku/83254/intel-nuc-kit-nuc5i5ryk/specifications.html) (Recomendado)  

Sensores:
- [Intel realsense d435I](https://www.intelrealsense.com/depth-camera-d435i/)
- [Robosense Helios 32-beam](https://www.robosense.ai/en/rslidar/RS-Helios)

Chassis:
- [Modelo 3D](https://github.com/AdrianCobo/perception_system/tree/main/meshes)
  <div align="center">
  <img width=500px src="https://github.com/AdrianCobo/my_bot/blob/main/imgs/mybot_mk2.jpg](https://github.com/user-attachments/assets/6268514e-7398-4a32-aca1-fb947f5899ed" alt="explode"></a>
  </div>
  
## Rosbags y memoria del TFG
Puedes encontrar la memoria del TFG de este proyecto y los rosbags grabados durante los experimentos [aquí](https://urjc-my.sharepoint.com/personal/josemiguel_guerrero_urjc_es/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fjosemiguel%5Fguerrero%5Furjc%5Fes%2FDocuments%2FRosbags%5FAdrian&ga=1)

## Problemas conocidos:
Si tienes problemas con la imu de la camara realsense d435I prueba a configurar las reglas udev:  
Posible mensaje de error: [realsense2_camera_node-1]  24/09 12:16:19,876 ERROR [138762487072320] (backend-v4l2.cpp:2970) xioctl(VIDIOC_QBUF) failed when requesting new frame! fd: 31 error: No such device  

[Solución](https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide?_ga=2.136179505.1802472520.1727172753-1313938100.1727172753)
**Sigue el tutorial solo hasta ejecutar el script**: ./scripts/setup_udev_rules.sh 

## ToDo
- Corregir inercias en los Xacro.
