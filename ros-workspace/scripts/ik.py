import argparse
import baxter_interface
import copy
import rospy
import sys
import time

from geometry_msgs.msg import (
        PoseStamped,
        Pose,
        Point,
        Quaternion,
)

from std_msgs.msg import Header

from baxter_core_msgs.srv import (
        SolvePositionIK,
        SolvePositionIKRequest,
        )

""" class that handles robot movement relative to the keyboard """

""" The width of a key on the keyboard, in meters"""
keyWidth = 0.0225

""" amount to press down on the key, in meters"""
pressHeight = 0.04

lowE = PoseStamped(
        header=Header(stamp=None, frame_id='base'),
        pose=Pose(
	position=Point(
		x=0.687579481614,
		y=0.1,
	        z=-0.09,),
	orientation=Quaternion(
		x=0.0,
		y=1.0,
 		z=0.0,
		w=0.0,
		),
	)
)

""" converts and index of a key to a pose"""
def index2position(i):
    pose = copy.deepcopy(lowE)
    pose.pose.position.y  = pose.pose.position.y + keyWidth * i
    return pose

"""converts a pose above the key to a pose pressing the key down"""
def pressedPos(pos):
    pose = copy.deepcopy(pos)
    pose.pose.position.z  = pose.pose.position.z - pressHeight
    return pose

""" Gets and ik solution for a given pose"""
def position2IK(pos):
    ns = "ExternalTools/left/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=None, frame_id='base')
    ikreq.pose_stamp.append(pos)

    try:
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Service call failed: %s" % (e,))
        return 1

    if (resp.isValid[0]):
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
	return limb_joints
    else:
    	return None
 
    return limb_joints

""" moves to a pose ( ik solution ) """
def movePose(pose, duration = 0.03):
        rospy.init_node("rsdk_ik_service_client")
        arm = baxter_interface.Limb('left')
	timeout = time.clock() + duration
	while not rospy.is_shutdown() and time.clock() < timeout:
        	arm.set_joint_positions(pose)
        	rospy.sleep(0.01)


def ik_test(limb):
    rospy.init_node("rsdk_ik_service_client")
    ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')

    poses = {
            'left': PoseStamped(
                header=hdr,
                pose=Pose(
                    position=Point(
                        x=0.8,
                        y=0.1,
                        z=0.0,
                        ),
                    orientation=Quaternion(
                        x=0.5,
                        y=0.5,
                        z=0.5,
                        w=0.5,
                        ),
                    ),
                ),
            'right': PoseStamped(
                header=hdr,
                pose=Pose(
                    position=Point(
                        x=0.756982770038,
                        y=-0.852598021641,
                        z=0.0388609422173,
                        ),
                    orientation=Quaternion(
                        x=0.367048116303,
                        y=0.885911751787,
                        z=-0.108908281936,
                        w=0.261868353356,
                        ),
                    ),
                ),
            }
    ikreq.pose_stamp.append(poses[limb])

    try:
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Service call failed: %s" % (e,))
        return 1

    if (resp.isValid[0]):
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
        arm = baxter_interface.Limb('left')
	while not rospy.is_shutdown():
        	arm.set_joint_positions(limb_joints)
        	rospy.sleep(0.01)
    else:
        print("INVALID POSE - No Valid Joint Solution Found.")
 
    return 0

def main():
    """RSDK Inverse Kinematics Example
 
   A simple example of using the Rethink Inverse Kinematics
   Service which returns the joint angles and validity for
   a requested Cartesian Pose.
 
   Run this example, passing the *limb* to test, and the
   example will call the Service with a sample Cartesian
   Pose, pre-defined in the example code, printing the
   response of whether a valid joint solution was found,
   and if so, the corresponding joint angles.
   """
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    parser.add_argument(
        '-l', '--limb', choices=['left', 'right'], required=False,
        help="the limb to test"
    )
    args = parser.parse_args(rospy.myargv()[1:])
    return ik_test('left')
 
if __name__ == '__main__':
    sys.exit(main())
