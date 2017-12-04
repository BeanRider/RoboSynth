import cv2
import Tkinter
import tkSnack
import ik
import CVNotes

# Detects note data using CVNotes
(frequencies, positions) = CVNotes.detect_notes()

# Plays notes
def setVolume(volume=50):
    """set the volume of the sound system"""
    if volume > 100:
        volume = 100
    elif volume < 0:
        volume = 0
    tkSnack.audio.play_gain(volume)


def playNote(freq, duration):
    """play a note of freq (hertz) for duration (seconds)"""
    snd = tkSnack.Sound()
    filt = tkSnack.Filter('generator', freq, 30000, 0.0, 'sine', int(11500 * duration))
    snd.stop()
    snd.play(filter=filt, blocking=1)


def soundStop():
    global root
    """stop the sound the hard way"""
    try:
        root = root.destroy()
        filt = None
    except:
        pass


root = Tkinter.Tk()
soundStop()

root.withdraw()

# have to initialize the sound system, required!!
tkSnack.initializeSnack(root)
# set the volume of the sound system (0 to 100%)
setVolume(30)
frequencies = map(lambda x: x * 2, frequencies)
for i in frequencies:
    playNote(i, 1)


poses = list()
for i in positions:
    above = ik.index2position(i)
    below = ik.pressedPos(above)
    poses.append(above)
    poses.append(below)
    poses.append(above)

iks = map(lambda x: ik.position2IK(x), poses)

for i in iks:
    ik.movePose(i)

cv2.waitKey(0)
