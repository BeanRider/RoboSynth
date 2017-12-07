import cv2
import Tkinter
from geometry_msgs.msg import (
        PoseStamped,
        Pose,
        Point,
        Quaternion,
)
from std_msgs.msg import Header


import tkSnack
import ik
import rospy
from geometry_msgs.msg import (
        PoseStamped,
        Pose,
        Point,
        Quaternion,
)
from std_msgs.msg import Header
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

hdr = Header(stamp=None, frame_id='base')
read_music_pose = PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=0.8,
                    y=0.1,
                    z=-0.05,
                    ),
                orientation=Quaternion(
                    x=0.5,
                    y=0.5,
                    z=0.5,
                    w=0.5,
                    ),
                ),
            ) 

instruction = (ik.position2IK(read_music_pose), 0.1)
print 'reading music'
ik.movePose(instruction[0], instruction[1])
    
data = rospy.wait_for_message("/cameras/left_hand_camera/image", Image)
cv_image = CvBridge().imgmsg_to_cv2(data, desired_encoding='passthrough')
cv2.imshow('image', cv_image)
cv2.imwrite('notes2.png', cv_image)
print 'done reading'

import CVNotes
# Detects note data using CVNotes
(frequencies, positions) = CVNotes.detect_notes()

print positions
ode = [8,8,7,6,6,7,8,9,10,10,9,8,8,9,9]

# # Plays notes
# def setVolume(volume=50):
#     """set the volume of the sound system"""
#     if volume > 100:
#         volume = 100
#     elif volume < 0:
#         volume = 0
#     tkSnack.audio.play_gain(volume)
# 
# 
# def playNote(freq, duration):
#     """play a note of freq (hertz) for duration (seconds)"""
#     snd = tkSnack.Sound()
#     filt = tkSnack.Filter('generator', freq, 30000, 0.0, 'sine', int(11500 * duration))
#     snd.stop()
#     snd.play(filter=filt, blocking=1)
# 
# 
# def soundStop():
#     global root
#     """stop the sound the hard way"""
#     try:
#         root = root.destroy()
#         filt = None
#     except:
#         pass
# 
# 
# root = Tkinter.Tk()
# soundStop()
# 
# # root.withdraw()
# 
# # have to initialize the sound system, required!!
# tkSnack.initializeSnack(root)
# # set the volume of the sound system (0 to 100%)
# setVolume(30)
# frequencies = map(lambda x: x * 2, frequencies)
# for i in frequencies:
#     playNote(i, 1)

poses = list()
for i in positions:
    above = ik.index2position(i)
    below = ik.pressedPos(above)
    poses.append((above, 0.04))
    poses.append((below, 0.04))
    poses.append((above, 0.01))


iks = map(lambda x: (ik.position2IK(x[0]), x[1]), poses)

iks.insert(0, (ik.position2IK(ik.index2position(3)), 0.2))

for i in iks:
    ik.movePose(i[0], i[1])

cv2.waitKey(0)
