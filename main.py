#### start webcam and detect movement ####

import cv2 
import streamlit as st
import time
import glob
import os 
from emailing import send_email
from datetime import datetime 

st.title('Motion Detector')
start = st.button('Start Camera')

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0) #set up camera 

    while True:
        check, frame = camera.read() # read first frame of video 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #get current time as a datetime object
        now = datetime.now()

        #get day and time and add them to the frame 
        cv2.putText(img=frame, text=now.strftime('%A'), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=now.strftime('%H:%M:%S'), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0),
                    thickness=2, lineType=cv2.LINE_AA)
        streamlit_image.image(frame)

video = cv2.VideoCapture(0)
time.sleep(1)

#get first frame variable 
first_frame = None 
status_list = []
count = 1

def clean_folder():
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)

while True:
    status = 0 
    check, frame = video.read()
    
    #convert frames to gray scale frames 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #blur method - provide frame, amt of blurness, and 0 
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    #first iteration it's None 
    if first_frame is None:
        first_frame = gray_frame_gau
    
    #now check difference 
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    
    #if its 10 or above, reassign val of 255 to that pixel
    thres_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1] #white pixels have a val of 30 or higher 
    #error????????????????????
    dil_frame = cv2.dilate(thres_frame, None, iterations=2) #higher num iteration, more processing applied
    cv2.imshow('My video', dil_frame)
    
    #find contours around white areas
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        #if it's a small object, like a fake obj, continue 
        if cv2.contourArea(contour) < 5000:
            continue
        #detect the movement 
        x, y, w, h = cv2.boundingRect(contour)
        #draw a rectangle around original frame 
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        #use .any() for an array with more than one element 
        if rectangle.any():
            status = 1 
            #store images
            cv2.imwrite(f'images/{count}.png', frame)
            count += 1 
            #produce a list of images
            all_images = glob.glob('images/*png')
            #get the one in the middle 
            index = int(len(all_images) // 2)
            image_with_object = all_images[index]

    status_list.append(status)
    #print status_list
    #update it to only contain the last 2 items 
        #because this is when it changes or doesn't change, aka detects movement
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_with_object)
        clean_folder()


    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) #creates a keyboard key object

    #if they press q key, break video 
    if key == ord('q'):
        break 

video.release()


