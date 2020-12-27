# -*- coding: utf-8  -*-
"""
Created on Sat Dec 12 12:20:23 2020

@author: Trent Smith
"""
import cv2
import speech_recognition as sr
import sqlite3
import pyttsx3
import flask
conn = sqlite3.connect(":memory:")
#basic crude functions
def create_table():
    conn.execute('''create table my_table (user text, name text, xml text)''')
# read text from your input file containing xml
def open_xml_file():
    f = open("buffer.xml")
    xml_string_from_file = f.read()
    f.close()
    return xml_string_from_file
def save_to_file(xml_string_from_file):
    f = open("buffer.xml","w")
    f.write(xml_string_from_file)
    f.close()
    print("test")
def insert_into_xml(user,name,xml_string):
    cur = conn.cursor()
    cur.execute('''insert into my_table (user, name, xml) values (?, ?, ?)''', (user, name, xml_string))
    conn.commit()
def select_from_table(user,name):
        sql_select_query = """select * from my_table where name = ? and user = ?"""
        records= conn.execute(sql_select_query,(name,user))
        for row in records:
            print("integer = " , row[0])
            print("name = ", row[1] )
            print("xml = ", row[2])
            response=row[2]
        return response
def addedtrainedcas(user,name):
    xml_string_from_file= open_xml_file()
    insert_into_xml(user, name, xml_string_from_file)
def update_xml_file(user,name):
    answer = select_from_table(user,name)
    print(answer)
    save_to_file(answer)
create_table()
################################
#add a file to the database
user = "trent"
name = "trent"
addedtrainedcas(user,name)
#update the file to find the current object
update_xml_file(user,name)
faceCascade = cv2.CascadeClassifier("buffer.xml")
#############################
def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))
#############################
cap = cv2.VideoCapture(0)
# parse with the XML parser of your choice
from xml.dom.minidom import parseString

r = sr.Recognizer()
engine = pyttsx3.init()

engine.say("Hello Trent How are you?")

engine.runAndWait()
with sr.Microphone() as source:
    print("Speak Anything :")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(format(text))
        if "testing" in format(text):
            print("success testing has")            
    except:
        print("Sorry could not recognize what you said")
'''
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
# When everything done, release the capture'''
cap.release()
cv2.destroyAllWindows()