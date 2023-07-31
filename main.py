#### start webcam and detect movement ####

import cv2 
import time

video = cv2.VideoCapture(0) #set up camera
check, frame = video.read() #read first frame of video 

print(check)
print(frame)

