# 🤖 Waypoint Navigator — ROS2 Autonomous Mission Planner

A ROS2 package for autonomous waypoint navigation using Nav2.
Define a sequence of goals in a YAML file and let the robot execute
the full mission and return to its starting position automatically.

Tested on the **Smart Camaro** — an Ackermann-steering autonomous
vehicle simulation developed at GIPAR/IFBA.

---

## ✨ Features

- Loads waypoints from an external YAML file (no recompilation needed)
- Sends goals sequentially to Nav2 via `NavigateToPose` action
- Automatically captures the initial pose via AMCL
- Retries failed goals up to N times (configurable)
- Skips unreachable waypoints and logs the failure
- Returns to starting position after completing the mission
- Publishes real-time mission status to `/mission/status`

---

## 📋 Requirements

- ROS2 Jazzy
- Nav2 (with AMCL localization)
- A working map and SLAM/localization pipeline

---

## 📁 Package Structure

    waypoint_navigator/
    ├── waypoint_navigator/
    │   └── mission_node.py      # Main mission execution node
    ├── config/
    │   └── waypoints.yaml       # Waypoint definitions
    ├── launch/
    │   └── mission.launch.py    # Launch file
    ├── package.xml
    └── setup.py

---

## 🚀 Usage

**1. Clone into your ROS2 workspace:**
    cd ~/your_ws/src
    git clone https://github.com/your-username/waypoint_navigator.git

**2. Build:**
    cd ~/your_ws
    colcon build --packages-select waypoint_navigator
    source install/setup.bash

**3. Edit your waypoints** in `config/waypoints.yaml`

**4. Run** (with your simulation and Nav2 already running):
    ros2 run waypoint_navigator mission_node \
      --ros-args -p waypoints_file:=/path/to/waypoints.yaml

---

## 📍 Waypoints YAML Format

    waypoints:
      - nome: "point_A"
        x: 2.0
        y: 1.5

      - nome: "point_B"
        x: 5.0
        y: 3.0

---

## 📡 Topics

| Topic | Type | Description |
|---|---|---|
| `/mission/status` | `std_msgs/String` | Real-time mission status |
| `/amcl_pose` | `geometry_msgs/PoseWithCovarianceStamped` | Used to capture initial pose |
| `/navigate_to_pose` | `nav2_msgs/NavigateToPose` | Nav2 action interface |

---

## ⚙️ Parameters

| Parameter | Default | Description |
|---|---|---|
| `waypoints_file` | `''` | Absolute path to the YAML file |
| `max_retries` | `3` | Max attempts per waypoint before skipping |

---

## 🏫 Context

This package was developed and tested on the **Smart Camaro**,
an Ackermann-steering autonomous vehicle simulation built with
ROS2 Jazzy + Gazebo Harmonic at
[GIPAR](https://github.com/gipar-ifba) — IFBA, Vitória da Conquista.

---

## 📄 License

MIT License
