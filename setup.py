from setuptools import setup
import os
from glob import glob

package_name = 'waypoint_navigator'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        # Registra o pacote no ROS2
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Inclui os arquivos de launch
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),

        # Inclui os arquivos de config
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Seu Nome',
    maintainer_email='seu@email.com',
    description='ROS2 autonomous waypoint navigation package.',
    license='MIT',
    entry_points={
        'console_scripts': [
            # Define o comando "mission_node" que o ROS2 vai reconhecer
            'mission_node = waypoint_navigator.mission_node:main',
        ],
    },
)