#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from __future__ import print_function
import cv2 as cv
import argparse
from playsound import playsound
import numpy as np
import time
capture = cv.VideoCapture(0)
backSub = cv.bgsegm.createBackgroundSubtractorMOG()

if not capture.isOpened:
    print('Unable to open webcam')
    exit(0)
count= [0,0,0,0,0]
while True:
    threshold = 10000
    ret, frame = capture.read()
    if frame is None:
        break
    text1 = 'What do you want for dinner?'
    text2 = 'Wave your hand to order in different blocks'
    text3 = 'Please try the middle bottom to start the order'
    
    fgMask = backSub.apply(frame)
    frame = frame[:,::-1]/255
    fgMask = fgMask[:,::-1]/255
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 360),cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    cv.rectangle(frame, (475, 0), (775, 300), (0, 255, 0), 2)##middle
    cv.rectangle(frame, (980, 0), (1280, 300), (0, 255, 0), 2)##right up
    cv.rectangle(frame, (10, 450), (310, 750), (0, 255, 0), 2)##left down
    cv.rectangle(frame, (980, 450), (1280, 750), (0, 255, 0), 2)##leftdown
    cv.rectangle(frame, (10, 0), (310, 300), (0, 255, 0), 2)##left up
  
    #middle
    if np.sum(fgMask[0:300,475:775])>threshold:
        count[0]+=1
        if count[0]>5:
            playsound('tonight.m4a')
            count= [0,0,0,0,0]
    #leftup
    if np.sum(fgMask[0:300,980:1280])>threshold:
        count[1]+=1
        if count[1]>5:
            playsound('ding.m4a')
            count= [0,0,0,0,0]
    #leftdown
    if np.sum(fgMask[450:750,980:1280])>threshold:
        count[2]+=1
        if count[2]>5:
            playsound('gold.m4a')
            count= [0,0,0,0,0]
    #rightup
    if np.sum(fgMask[0:300,10:310])>threshold:
        count[3]+=1
        if count[3]>5:
            playsound('star.m4a')
            count= [0,0,0,0,0]
    #rightdown
    if np.sum(fgMask[450:750,10:310])>threshold:
        count[4]+=1
        if count[4]>5:
            playsound('bean.m4a')
            count= [0,0,0,0,0]

    cv.putText(frame, text1, (360,620 ), cv.FONT_HERSHEY_DUPLEX,1, (0, 255, 255), 1, cv.LINE_AA)
    cv.putText(frame, text2, (340,660 ), cv.FONT_HERSHEY_DUPLEX,1, (0, 255, 255), 1, cv.LINE_AA)
    cv.putText(frame, text3, (310,700 ), cv.FONT_HERSHEY_DUPLEX,1, (0, 255, 255), 1, cv.LINE_AA)
    frame = cv.resize(frame, (960, 540))
    window = 'Frame'
    cv.namedWindow(window)        # Create a named window    
    cv.moveWindow(window, 10,10)
    cv.imshow(window, frame)
    #cv.imshow('FG Mask', fgMask)
    
    keyboard = cv.waitKey(30)
    if  keyboard == 27:
        break
        
# 釋放攝影機
capture.release()

# 關閉所有 OpenCV 視窗
cv.destroyAllWindows()

