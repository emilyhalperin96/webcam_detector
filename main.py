#### start webcam and detect movement ####

import cv2 
import time


video = cv2.VideoCapture(0) #set up camera
time.sleep(1) # wait one second for the camera to load 

while True:
    check, frame = video.read() #read first frame of video 
    cv2.imshow('My video', frame)

    key = cv2.waitKey(1) #creates a keyboard key object

    #if they press q key, break video 
    if key == ord('q'):
        break 

video.release()


