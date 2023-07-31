#### start webcam and detect movement ####

import cv2 
import time


video = cv2.VideoCapture(0) #set up camera
time.sleep(1) # wait one second for the camera to load 

while True:
    check, frame = video.read() #read first frame of video 

    #convert frames to gray scale frames 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #blur method - provide frame, amt of blurness, and 0 
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    cv2.imshow('My video', gray_frame_gau)

    key = cv2.waitKey(1) #creates a keyboard key object

    #if they press q key, break video 
    if key == ord('q'):
        break 

video.release()


