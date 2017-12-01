import cv2
import numpy as np
import Tkinter
import tkSnack
import ik

notes_size = 10;

notes_color = cv2.imread('notes2.png')
notes = cv2.imread('notes2.png', 0)

edges = cv2.Canny(notes, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

ledger_lines = list()
width = notes.shape[1] * 0.95

for i in range(0,10):
  for rho,theta in lines[i]:
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a*rho
      y0 = b*rho
      x1 = int(x0 + width*(-b))
      y1 = int(y0 + width*(a))
      x2 = int(x0 - width*(-b))
      y2 = int(y0 - width*(a))
      ledger_lines.append((x1,x2,y1,y2))
      for i in range(0,1000):
          xcoor = x1 + (int)((x2-x1)*i/1000.0)
          ycoor = y1 + (int)((y2-y1)*i/1000.0) 
          if(len(filter(lambda x: not(x > 254), 
              map(lambda x : notes[ycoor + x, xcoor], [-6,6]))) ==0):
              cv2.circle(notes, 
                  (xcoor,ycoor), 
                  6, 
                  (255,255,255), 
                  -1)

kernel = np.ones((20,20),np.float32)/400
notes = cv2.filter2D(notes,-1,kernel)

cv2.imshow("notes for reaing", notes);

params = cv2.SimpleBlobDetector_Params()
params.filterByArea=True
params.filterByInertia=True
params.filterByConvexity = True
params.minArea=800
params.minInertiaRatio=0.35
params.minConvexity=.965

detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(notes);
keypoints = filter(lambda x: x.size > notes_size, keypoints)
keypoints.sort(key=lambda x: x.pt[0])

ledger_lines.sort(key=lambda x: (x[2] + x[3])/2)

real_ledger_lines = list()
for i in range(0,10,2):
    element = list()
    for j in range(0,4):
        element.append((ledger_lines[i][j] + ledger_lines[i+1][j])/2)
    real_ledger_lines.append(element)

for i in real_ledger_lines:
    cv2.line(notes_color,(i[0], i[2]),(i[1], i[3]),(0,0,255),1)

tones = list()
positions = list()

key = [ 349.2282, 329.6276, 293.6648, 261.6256, 246.9417, 220.0000, 195.9977, 174.6141, 164.8138, ]
         
for i in keypoints:
	notex = i.pt[0]
	notey = i.pt[1]
 
	cv2.circle(notes_color, (int(notex), int(notey)), 3, (255,255,0), -1)
 
	thresholds = list()
	for j in real_ledger_lines:
		slope = 1.0*(j[3] - j[2])/(j[1] - j[0])
		thresh = j[2] + slope*(notex - j[0])
		thresholds.append(thresh)
 
	thresholds.sort()
 
	for j in range(0, len(thresholds) - 1):
		thresholds.append((thresholds[j] + thresholds[j+1])/2)
 
	thresholds.sort()
 
	for j in range(0, len(thresholds)):
		cv2.circle(notes_color, (int(notex), int(thresholds[j])), 2, (255,0,13 * j), -1)
 
	dists = map(lambda x: abs(x - notey), thresholds)
	note = np.argmin(dists)
	positions.append(note)
	tones.append(key[note])

cv2.imshow('notes', notes_color)
print tones

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
    filt = tkSnack.Filter('generator', freq, 30000, 0.0, 'sine', int(11500*duration))
    snd.stop()
    snd.play(filter=filt, blocking=1)
def soundStop():
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
tones = map(lambda x: x*2, tones)
for i in tones:
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
