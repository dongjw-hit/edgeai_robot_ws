#!/bin/bash

cd ~/edgeai_robot_ws || exit 1

source install/setup.bash

echo "Stopping old Gazebo / ROS 2 / RViz processes..."

pkill -f "gz sim" 2>/dev/null
pkill -f "robot_state_publisher" 2>/dev/null
pkill -f "ros_gz_bridge" 2>/dev/null
pkill -f "ros_gz_sim" 2>/dev/null
pkill -f "rviz2" 2>/dev/null

sleep 2

echo "Starting realistic robot simulation..."

ros2 launch edgeai_robot_description simulation_real.launch.py &

SIM_PID=$!

sleep 5

echo "Starting RViz with realistic robot configuration..."

rviz2 -d \
~/edgeai_robot_ws/src/edgeai_robot_description/rviz/realistic_robot.rviz &

wait $SIM_PID
