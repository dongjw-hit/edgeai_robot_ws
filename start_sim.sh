#!/usr/bin/env bash

cd ~/edgeai_robot_ws

pkill -f "gz sim" 2>/dev/null || true
pkill -f robot_state_publisher 2>/dev/null || true
pkill -f ros_gz_bridge 2>/dev/null || true
pkill -f "ros_gz_sim create" 2>/dev/null || true

sleep 1

pixi run bash -lc '
source install/setup.bash
ros2 launch edgeai_robot_description simulation.launch.py
'
