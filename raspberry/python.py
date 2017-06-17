import sys
sys.path.append('/usr/local/lib/python3.4/site-packages')
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from flask import Flask, request
import time
import os
from os import listdir
app = Flask(__name__)
import requests
from threading import Thread

url = 'http://192.168.0.105:5000'
path = '/home/pi/Desktop/frames/'



'''@app.route('/get_img', methods=['POST'])
def draw_test():
        if request.method == 'POST':
                print("Someone send POST request\n")
                camera = PiCamera()
                rawCapture = PiRGBArray(camera)
                camera.close()
                time.sleep(0.1)
                camera.capture(rawCapture, format="bgr")
                frame = rawCapture.array
                timeNow = str(time.time())
                cv2.imwrite('/home/pi/Desktop/frames/'+timeNow+'.jpg',frame)
                rawCapture.truncate(0)
                requests.post('http://localhost:5000/send_img')
                return ""
'''

@app.route('/send_img', methods=['POST'])
def send_from_folder():
        if request.method == 'POST':
                for x in listdir(path):
                        files = {'name':x , 'file' : open(path+x,'rb')}
                        requests.post(url+'/receive_frame',files=files)
                        os.remove(path+x)
                        print(x)
                return ""
                

if (__name__ == '__main__'):
    app.run(host='0.0.0.0')
    
