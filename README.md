# RoboSynth

# ROS Server (Using ROS Lunar)
### 1. Setup the SDK
`cd ros-workspace`

`vim baxter.sh`

Change `baxter_hostname` to the Baxter robot serial name,

and `your_ip` to the host device IP (`ifconfig`).


### 2. Init the SDK:
`cd ros-workspace`

`chmod u+x baxter.sh`

`./baxter.sh`

### 3. To build the packages:
run `catkin_make`

### 4. start ROS core framework:
run `roscore`

### 5. the publisher (produces the notes):
run `rosrun tutorial_server talker.py`

### 6 the subscriber (listens for the notes):
run `rosrun tutorial_server listener.py`

# running the robot in simulation
`./baxter_sim`

`roslaunch baxter_gazebo baxter_world.launch`

`rosrun baxter_tools enable_robot.py -e`

`rosrun baxter_interface joint_trajectory_action_server.py`

`roslaunch baxter_moveit_config baxter_grippers.launch`

