import sys
import copy
import rospy
import moveit_msgs.msg
import geometry_msgs.msg
import moveit_commander

print "============ starting up"
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                        anonymous=False)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("left_arm")

print "============ Generating plan 1"
pose_target = geometry_msgs.msg.Pose();
#group.set_pose_reference_frame("/world")
# pose_target.pose.orientation.x = -0.27
# pose_target.pose.orientation.y = 0.65
# pose_target.pose.orientation.z = 0.27
print group.get_current_pose()
pose_target.orientation.x= -0.270598649982
pose_target.orientation.y= 0.653281233946
pose_target.orientation.z= 0.270598649992

pose_target.orientation.w = 0.65
pose_target.position.x = 0.909
pose_target.position.y = 1.102
pose_target.position.z = 0.321
group.set_pose_target(pose_target)

plan1 = group.plan()
group.go(wait=True)

print group.get_current_pose()
print "script done"
print group.get_planning_frame()
print group.get_end_effector_link()

import code
code.interact(local=locals())
