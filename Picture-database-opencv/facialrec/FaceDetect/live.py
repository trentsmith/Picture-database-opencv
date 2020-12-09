import time

import cv2
import numpy as np
from imutils.video import VideoStream
import imutils
import sqlite3
import pyttsx3
# connect to database and create table
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute('''create table my_table (name text, cates text, xml text)''')
# read text from your input file containing xml
f = open("haarcascade_frontalface_default.xml")
print(type(f))
xml_string_from_file = f.read()
print(type(xml_string_from_file))
# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")# insert text into database
cur = conn.cursor()
#note to drop table to delete this instance
#cur.execute('''insert into my_table (value1, value2, xml) values (?, ?, ?)''', (23, 42, xml_string_from_file))
conn.commit()
#s = cur.execute('''Select * from my_table''')
# read from database into variable
#xml_string_from_db = cur.fetchone()[2]
# parse with the XML parser of your choice
from xml.dom.minidom import parseString
# Are we using the Pi Camera?
usingPiCamera = True
# Set initial frame size.
frameSize = (320, 240)

# Initialize mutithreading the video stream.
vs = VideoStream(src=0, usePiCamera=usingPiCamera, resolution=frameSize,
        framerate=32).start()
# Allow the camera to warm up.
time.sleep(2.0)

timeCheck = time.time()
while True:
    # Get the next frame.
    frame = vs.read()
    # If using a webcam instead of the Pi Camera,
    # we take the extra step to change frame size.
    if not usingPiCamera:
        frame = imutils.resize(frame, width=frameSize[0])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret = frame
# Detect faces in the image
    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
 #flags = cv2.CV_HAAR_SCALE_IMAGE
 )
    print("Found {0} faces!".format(len(faces)))
 # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
 # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    print(1/(time.time() - timeCheck))
    timeCheck = time.time()

# When everything done, release the capture
cv2.destroyAllWindows()
vs.stop()