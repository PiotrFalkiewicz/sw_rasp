import sys
sys.path.append('/usr/local/lib/python3.4/site-packages')
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import os
import requests
import time


def areSimilar(x,y,z):
    threshold = 10
    if np.abs(x - y) < threshold:
        if np.abs(x - z) < threshold:
            if np.abs(y - z) < threshold:
                return True
    return False

start = True
lastMean = (0,0,0)

while True:
    try:
        camera = PiCamera()
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        camera.close()
        frame = rawCapture.array
        thisMean = (np.mean(frame[:,:,0]),np.mean(frame[:,:,1]),np.mean(frame[:,:,2]))
        if start:
            start = False
        else:
            x = np.subtract(lastMean,thisMean)
            sum = 0
            for y in x:
                sum += y*y
            path = '/home/pi/Desktop/msg/'
            checkFiles = os.listdir(path)
            if len(checkFiles)>0:
                print("Sending current frame")
                timeNow = str(time.time())
                cv2.imwrite('/home/pi/Desktop/frames/'+timeNow+'.jpg',frame)
                requests.post('http://localhost:5000/send_img')
                for y in checkFiles:
                    os.remove(path+y)
            elif sum > 1000 and not areSimilar(x[0],x[1],x[2]):
                print("Move detected. Difference: {}".format(sum))
                timeNow = str(time.time())
                cv2.imwrite('/home/pi/Desktop/frames/'+timeNow+'.jpg',frame)
                requests.post('http://localhost:5000/send_img')
                
    finally:

        lastMean = thisMean    
