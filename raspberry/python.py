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



@app.route('/get_img', methods=['POST'])
def draw_test():
        if request.method == 'POST':
                img = np.zeros(shape=(1,1),dtype=np.uint8)
                print("Someone send current frame request\n")
                cv2.imwrite('/home/pi/Desktop/msg/msg.jpg',img)
                return ""


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
    
