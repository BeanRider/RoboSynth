import rospy
from std_msgs.msg import String
import json

import baxter_interface
from baxter_interface import CHECK_VERSION

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

# TODO configure the note positions.
note_to_pos = {
        "A": Point(x=0, y=0, z=0),
        "B": Point(x=0, y=0, z=0),
        "C": Point(x=0, y=0, z=0),
        "D": Point(x=0, y=0, z=0),
        "E": Point(x=0, y=0, z=0),
        "F": Point(x=0, y=0, z=0),
        "G": Point(x=0, y=0, z=0)}

# TODO configure the default goal orientation
goal_ori = Quaternion(x=0, y=0, z=0, w=0)

def get_note_to_joint():
    """
    Uses the note_to_pos to find inverse kinematics solutions for each key, using the Baxter service.
    :return: a dictionary with String keys (notes) mapped to joint configs
    """
    note_to_q = {}

    for note, goal_pos in note_to_pos.iteritems():

        service_name = "ExternalTools/left/PositionKinematicsNode/IKService"
        iksvc = rospy.ServiceProxy(service_name, SolvePositionIK)
        ikreq = SolvePositionIKRequest()
        hdr = Header(stamp=rospy.Time.now(), frame_id="base")
        poses = {
            "left": PoseStamped(
                header=hdr,
                pose=Pose(position=goal_pos, orientation=goal_ori),
            ),
            "right": PoseStamped(
                header=hdr,
                pose=Pose(position=goal_pos, orientation=goal_ori),
            ),
        }

        ikreq.pose_stamp.append(poses[limb])
        try:
            rospy.wait_for_service(service_name, 5.0)
            resp = iksvc(ikreq)
        except (rospy.ServiceException, rospy.ROSException) as e:
            rospy.logerr("Service call failed: %s " % (e,))
            return 1

        if resp.isValid[0]:
            print("Success - solution found for note " + note)
            q = dict(zip(resp.joints[0].name, resp.joints[0].position))
            print(q)
        else:
            print("Failed to find a valid joint solution.")

        note_to_q[note] = q

    print(note_to_q)
    return note_to_q


def convert_notes_to_joint_pos(start_joint, notes):
    """
    Uses the computed joint configurations for each note to create an array of joint configs that will play the given
    list of notes, by moving to a note, and moving back to the start joint position (start_joint)
    :param start_joint: staring position to return to after playing a note.
    :param notes: array of Strings (notes to play)
    :return: an array of joint configs in order for Baxter to play the given list of notes.
    """
    note_to_joint = get_note_to_joint()
    to_return_joints = []

    for note in notes:
        to_return_joints.append(start_joint)
        to_return_joints.append(note_to_joint[note])

    to_return_joints.append(start_joint)
    return to_return_joints
