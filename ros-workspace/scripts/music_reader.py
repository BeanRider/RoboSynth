#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import ik
import cv2
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import (
        PoseStamped,
        Pose,
        Point,
        Quaternion,
)
from std_msgs.msg import Header
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    data = rospy.wait_for_message("/cameras/left_hand_camera/image", image)
    cv_image = cvbridge().imgmsg_to_cv2(data, desired_encoding='passthrough')
    cv2.imshow('image', cv_image)
    cv2.imwrite('notes2.png', cv_image)


if __name__ == '__main__':
    listener()

