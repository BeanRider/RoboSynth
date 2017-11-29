import argparse
import sys
import time

import rospy
import baxter_interface
import copy

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

keyWidth = 0.1222

pressHeight = 0.3

lowE = PoseStamped(
        header=Header(stamp=None, frame_id='base'),
        pose=Pose(
	position=Point(
		x=0.687579481614,
		y=0.1,
		z=0.1088352386502,
    		),
	orientation=Quaternion(
		x=-0.366894936773,
		y=0.885980397775,
 		z=0.108155782462,
		w=0.262162481772,
		),
	)
)

def index2position(i):
    pose = copy.deepcopy(lowE)
    pose.pose.position.y  = pose.pose.position.y + keyWidth * i
    return pose

def pressedPos(pos):
    pose = copy.deepcopy(pos)
    pose.pose.position.z  = pose.pose.position.z - pressHeight
    return pose

def position2IK(pos):
    print 'finding ik'
    ns = "ExternalTools/left/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=None, frame_id='base')
    ikreq.pose_stamp.append(pos)

    try:
        print "calling service"
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Service call failed: %s" % (e,))
        return 1

    if (resp.isValid[0]):
        print("SUCCESS - Valid Joint Solution Found:")
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
	return limb_joints
    else:
    	return None
 
    return limb_joints

def movePose(pose):
        rospy.init_node("rsdk_ik_service_client")
        arm = baxter_interface.Limb('left')
	timeout = time.clock() + 0.2
	while not rospy.is_shutdown() and time.clock() < timeout:
		print time.clock() - timeout
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
                        x=0.687579481614,
                        y=0.1,
                        z=0.1088352386502,
                        ),
                    orientation=Quaternion(
                        x=-0.366894936773,
                        y=0.885980397775,
                        z=0.108155782462,
                        w=0.262162481772,
                        ),
                    ),
                ),
            'right': PoseStamped(
                header=hdr,
                pose=Pose(
                    position=Point(
                        x=0.656982770038,
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
        print "calling service"
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Service call failed: %s" % (e,))
        return 1

    if (resp.isValid[0]):
        print("SUCCESS - Valid Joint Solution Found:")
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
        print limb_joints
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
