import picamera
import psutil
import os
from bluedot import BlueDot
import time
bd = BlueDot()
bd.wait_for_connection
# delete oldest files until we reach 10 or folder is empty
def deleteVids():
    i = 0
    delVids = 0

    print("Deleting 10 old files")

    while (delVids < 10) and (len(os.listdir("/home/pi/PiDash/videos")) > 0):
        if os.path.isfile("/home/pi/PiDash/videos/vid%s.h264" % i):
            os.remove("/home/pi/PiDash/videos/vid%s.h264" % i)
            delVids = 0
        i += 1

if(psutil.disk_usage(".").percent > 85):
    print("Low space, deleting old files")
    deleteVids()

# if vidIndex file doesn't exist, create and set index to 0
if not os.path.exists("/home/pi/PiDash/vidIndex.txt"):
    with open("/home/pi/PiDash/vidIndex.txt", "w") as f:
        f.write('1')

# incrementing vidIndex.txt and setting path for new file
with open("/home/pi/PiDash/vidIndex.txt", "r") as f:
    vidIndex = int(f.read())

with open("/home/pi/PiDash/vidIndex.txt", "w") as f:
    f.write(str(vidIndex + 1))    

newFile = "/home/pi/PiDash/videos/vid%s.h264" % vidIndex

# initializing camera object, setting resolution to 1080p and framerate to 30fps
with picamera.PiCamera() as cam:
    cam.framerate = 25
    cam.resolution = (1920,1080)

# while recording check for "quit" button activity, and hard drive space
    recording = True
    cam.start_recording(newFile)
    while recording:
        if psutil.disk_usage(".").percent > 85: 
            print("Low space, deleting old files")
            deleteVids()

# if button is currently held, set end recording loop
        recording = not bd.is_pressed
        cam.wait_recording(5)

    cam.stop_recording()
