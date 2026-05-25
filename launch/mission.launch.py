from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os


def generate_launch_description():

    # Argumento para o caminho do arquivo de waypoints
    waypoints_file_arg = DeclareLaunchArgument(
        'waypoints_file',
        default_value=os.path.join(
            # Pega o diretório do pacote automaticamente
            os.path.dirname(__file__),
            '..', 'config', 'waypoints.yaml'
        ),
        description='Caminho para o arquivo de waypoints'
    )

    # Argumento para número de tentativas por waypoint
    max_retries_arg = DeclareLaunchArgument(
        'max_retries',
        default_value='3',
        description='Número máximo de tentativas por waypoint'
    )

    # Nó principal da missão
    mission_node = Node(
        package='waypoint_navigator',
        executable='mission_node',
        name='mission_node',
        output='screen',
        parameters=[{
            'waypoints_file': LaunchConfiguration('waypoints_file'),
            'max_retries': LaunchConfiguration('max_retries'),
        }]
    )

    return LaunchDescription([
        waypoints_file_arg,
        max_retries_arg,
        mission_node,
    ])