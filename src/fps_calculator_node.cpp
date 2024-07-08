/*
# Copyright (c) 2024 Adrián Cobo Merino
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
*/

#include "rclcpp/rclcpp.hpp"
#include <opencv2/opencv.hpp>
#include "cv_bridge/cv_bridge.h"
#include "sensor_msgs/msg/image.hpp"
#include <time.h>
#include <iostream>
#include <fstream>
 
using namespace cv;
using namespace std;
std::ofstream FPS_DATA_FILE("/home/ir/Desktop/ros2_ws/src/perception_system/data/FPS.txt"); // Record FPS Data File

class FpsCalculator : public rclcpp::Node
{
public:
  FpsCalculator()
  : Node("opencv_subscriber")
  {
    auto qos = rclcpp::QoS(rclcpp::QoSInitialization(RMW_QOS_POLICY_HISTORY_KEEP_LAST, 5));
    qos.reliability(RMW_QOS_POLICY_RELIABILITY_RELIABLE);
    frames_obtained_ = 0;

    subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
      "/camera/camera/color/image_raw", qos,
      std::bind(&FpsCalculator::count_frames_callback, this, std::placeholders::_1));
  }

  int frames_obtained_;

private:
  void count_frames_callback(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    if(frames_obtained_ == 0){
        // Start Time
        time(&start);
        frames_obtained_++;
    }else if(frames_obtained_ == 30){
        // End Time
        time(&end);

        // Time elapsed
        double seconds = difftime (end, start);
        cout << "Time taken : " << seconds << " seconds" << endl;
    
        // Calculate frames per second
        int fps  = (int)(frames_obtained_ / seconds);
        cout << "Estimated frames per second : " << fps << endl;
        
        // uncomment next lines for recording data
        FPS_DATA_FILE << fps << std::endl;
        frames_obtained_ = 0;
    }else{
        frames_obtained_++;
    }
  }

  time_t start, end;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;
};

 
int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FpsCalculator>());
    rclcpp::shutdown();
    FPS_DATA_FILE.close();

    return 0;
}
