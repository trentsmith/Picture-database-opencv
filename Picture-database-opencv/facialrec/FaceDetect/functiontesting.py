# -*- coding: utf-8 -*-
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
  conn.execute('CREATE TABLE IF NOT EXISTS nameandparts(name TEXT, parts TEXT)')
  conn.execute('CREATE TABLE IF NOT EXISTS picsandparts(parts TEXT, xmlstrings TEXT)')
def listToString(s): 
    # initialize an empty string 
    str1 = " " 
    # return string   
    return (str1.join(s)) 
def insert_value_into_tablenameparts(name,parts):
  conn.execute('INSERT INTO nameandparts(name,parts)VALUES(?,?)',(name,parts))
  conn.commit()
def insert_value_into_tablepicsandparts(part,xml):
  conn.execute('INSERT INTO picsandparts(parts,xmlstrings)VALUES(?,?)',(part,xml))
  conn.commit()
def select_from_table(name):
        sql_select_query = """select parts from nameandparts where name = ?"""
        records = conn.execute(sql_select_query, (name,))
        #records = conn.fetchall()
        print("Printing ID ", name)
        for row in records:
            print("keywords = " , row[0])
            response=row[0]
            # print("user = ", row[2])
        parts = response.split(" ")
        print(parts)
        for part in parts:
          sql_select_query = """select xmlstrings from picsandparts where parts = ?"""
          #conn.execute(sql_select_query, (part,))
          records = conn.execute(sql_select_query, (part,))
          for row in records:
              print("Printing ID ", row)
              if(len(row)>0):
                  return row[0]
def open_xml_file():
    f = open("haarcascade_frontalface_default.xml")
    xml_string_from_file = f.read()
    f.close()
    return xml_string_from_file
def save_to_file(xml_string_from_file):
    f = open("buffer.xml","w")
    f.write(xml_string_from_file)
    f.close()
def addedtrainedcas(name,parts):
    insert_value_into_tablenameparts(name,parts)
    xml_string_from_file= open_xml_file()
    partss= parts.split(" ")
    for part in partss:
        insert_value_into_tablepicsandparts(part,xml_string_from_file)
def update_xml_file(name):
    answer = select_from_table(name)
    print(answer)
    save_to_file(answer)
create_table()
################################
#add a file to the database
user = "Trent"
name = "Trent head"
addedtrainedcas(user,name)
#update the file to find the current object
faceCascade = cv2.CascadeClassifier("buffer.xml")
select_from_table(user)
#############################
cap = cv2.VideoCapture(0)
# parse with the XML parser of your choice
from xml.dom.minidom import parseString
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
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()