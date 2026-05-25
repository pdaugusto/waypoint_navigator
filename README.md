# 🤖 Waypoint Navigator — ROS2 Autonomous Mission Planner

A ROS2 package for autonomous waypoint navigation using Nav2.  
Define a sequence of goals in a YAML file and let the robot execute the full mission and return to its starting position automatically.

> Tested on the **Smart Camaro** — an Ackermann-steering autonomous vehicle simulation developed at [GIPAR](https://github.com/gipar-ifba) / IFBA, Vitória da Conquista.

---

## ✨ Features

- Loads waypoints from an external YAML file — no recompilation needed
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

```
waypoint_navigator/
├── waypoint_navigator/
│   └── mission_node.py      # Main mission execution node
├── config/
│   └── waypoints.yaml       # Waypoint definitions
├── launch/
│   └── mission.launch.py    # Launch file
├── resource/
│   └── waypoint_navigator   # ROS2 package index file (empty)
├── package.xml
├── setup.py
└── README.md
```

---

## 🚀 Installation

```bash
# 1. Clone into your ROS2 workspace
cd ~/your_ws/src
git clone https://github.com/your-username/waypoint_navigator.git

# 2. Install dependencies
cd ~/your_ws
rosdep install --from-paths src --ignore-src -r -y

# 3. Build
colcon build --packages-select waypoint_navigator

# 4. Source
source install/setup.bash
```

---

## 📍 Defining Waypoints

Edit `config/waypoints.yaml` with the coordinates you want the robot to visit:

```yaml
waypoints:
  - nome: "point_A"
    x: 2.0
    y: 1.5
    oz: 0.0
    ow: 1.0

  - nome: "point_B"
    x: 5.0
    y: 3.0
    oz: 0.707
    ow: 0.707
```

> **Tip:** Hover over any point on the map in RViz2 to get the `x` and `y` coordinates from the bottom panel.  
> `oz` and `ow` define the final orientation — optional, defaults to no rotation.

---

## ▶️ Running

Make sure your simulation and Nav2 are already running before launching the mission.

```bash
# Option 1 — using the default waypoints.yaml
ros2 launch waypoint_navigator mission.launch.py

# Option 2 — using a custom waypoints file
ros2 launch waypoint_navigator mission.launch.py \
  waypoints_file:=/absolute/path/to/your/waypoints.yaml

# Option 3 — running the node directly
ros2 run waypoint_navigator mission_node \
  --ros-args -p waypoints_file:=/absolute/path/to/waypoints.yaml
```

---

## 📡 Monitoring the Mission

```bash
# Watch mission status in real time
ros2 topic echo /mission/status

# Check if the node is running
ros2 node list

# List active topics
ros2 topic list
```

---

## ⚙️ Parameters

| Parameter | Default | Description |
|---|---|---|
| `waypoints_file` | `config/waypoints.yaml` | Path to the YAML waypoints file |
| `max_retries` | `3` | Max attempts per waypoint before skipping |

```bash
# Example: change max_retries at launch
ros2 launch waypoint_navigator mission.launch.py max_retries:=5
```

---

## 📡 Topics

| Topic | Type | Description |
|---|---|---|
| `/mission/status` | `std_msgs/String` | Real-time mission status |
| `/amcl_pose` | `geometry_msgs/PoseWithCovarianceStamped` | Used to capture initial pose |
| `/navigate_to_pose` | `nav2_msgs/NavigateToPose` | Nav2 action interface |

---

## 🔄 Mission Flow

```
Start
  │
  ▼
Capture initial pose (via /amcl_pose)
  │
  ▼
Navigate to waypoint 1 ──► Failed after retries? ──► Skip + log
  │
  ▼
Navigate to waypoint 2 ──► ...
  │
  ▼
Navigate to waypoint N
  │
  ▼
Return to starting position
  │
  ▼
Mission complete ✅
```

---

## 🏫 Context

This package was developed and tested on the **Smart Camaro**, an Ackermann-steering autonomous vehicle simulation built with ROS2 Jazzy + Gazebo Harmonic at [GIPAR](https://github.com/gipar-ifba) — IFBA, Vitória da Conquista.

---

## 📄 License

MIT License