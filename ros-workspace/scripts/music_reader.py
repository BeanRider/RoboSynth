#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

def callback(data):
    cv_image = CvBridge().imgmsg_to_cv2(data, desired_encoding='passthrough')
    cv2.imshow('image', cv_image)
    cv2.imwrite('notes2.png', cv_image)
    cv2.waitKey(0)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('music_reader', anonymous=True)

    rospy.Subscriber("/cameras/left_hand_camera/image", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
