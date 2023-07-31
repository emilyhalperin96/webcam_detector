#### start webcam and detect movement ####

import cv2 
import time


video = cv2.VideoCapture(0) #set up camera
time.sleep(1) # wait one second for the camera to load 


#get first frame variable 
first_frame = None 

while True:
    check, frame = video.read() #read first frame of video 

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
    dil_frame = cv2.dilate(thres_frame, None, iterations=2) #higher num iteration, more processing applied
    cv2.imshow('My video', dil_frame)
    
    #find contours around white areas
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        #if it's a small object, like a fake obj, continue 
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        #draw a rectangle around original frame 
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) #creates a keyboard key object

    #if they press q key, break video 
    if key == ord('q'):
        break 

video.release()


