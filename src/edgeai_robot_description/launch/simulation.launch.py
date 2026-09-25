import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import xacro


def generate_launch_description():

    # ---------------------------------------------------------
    # Package paths
    # ---------------------------------------------------------
    package_name = 'edgeai_robot_description'

    pkg_share = get_package_share_directory(package_name)
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    xacro_file = os.path.join(
        pkg_share,
        'urdf',
        'edgeai_robot.urdf.xacro'
    )

    world_file = os.path.join(
    pkg_share,
    'worlds',
    'empty.sdf'
    )

    # ---------------------------------------------------------
    # Convert Xacro to robot_description
    # ---------------------------------------------------------
    robot_description_config = xacro.process_file(xacro_file)

    robot_description = {
        'robot_description': robot_description_config.toxml()
    }

    # ---------------------------------------------------------
    # Start Gazebo Harmonic
    # ---------------------------------------------------------
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': f'-r {world_file}'
        }.items()
    )

    # ---------------------------------------------------------
    # robot_state_publisher
    # ---------------------------------------------------------
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # ---------------------------------------------------------
    # Spawn robot
    # ---------------------------------------------------------
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'edgeai_robot',
            '-topic', 'robot_description',
            '-x', '-1.5',
            '-y', '-1.5',
            '-z', '0.10'
        ],
        output='screen'
    )

    # ---------------------------------------------------------
    # ROS 2 <-> Gazebo bridges
    # ---------------------------------------------------------
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        arguments=[
            # Robot motion
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',

            # LiDAR
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',

            # RGB-D Camera
            '/camera/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/depth_image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'
        ],
        output='screen'
    )

    # ---------------------------------------------------------
    # RViz
    # ---------------------------------------------------------
    rviz_config = os.path.join(
        pkg_share,
        'rviz',
        'edgeai_robot.rviz'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    # ---------------------------------------------------------
    # Launch everything
    # ---------------------------------------------------------
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        bridge,
        rviz
    ])
