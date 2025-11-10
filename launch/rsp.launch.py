import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Configuración del tiempo simulado
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Ruta al paquete y archivo xacro
    pkg_path = os.path.join(get_package_share_directory('my_package'))
    xacro_file = os.path.join(pkg_path, 'robot_description', 'robot.urdf.xacro')

    # Procesar el archivo xacro
    robot_description_config = xacro.process_file(xacro_file)
    params = {
        'robot_description': robot_description_config.toxml(),
        'use_sim_time': use_sim_time
    }

    # Nodo: joint_state_publisher_gui (simula encoders)
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # Nodo: robot_state_publisher (publica los TFs)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Retornar LaunchDescription
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'
        ),
        joint_state_publisher_node,
        robot_state_publisher_node
    ])
