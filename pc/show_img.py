from flask import Flask, request

app = Flask(__name__)
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2


@app.route('/main.html', methods=['GET'])
def showCollection():
    site = "<html><head><title>View from Camera</title></head>"
    site += "<body><table>"
    path = '/home/piotr/PycharmProjects/untitled3/static/'
    collection = listdir(path)
    collection.sort()
    i = 0
    site += "<tr>"
    for node in collection:

        if i % 8 == 0:
            site += "</tr><tr>"
        if isfile(join(path, node)):
            site += "<td><img width=160 height=120 src=" + '/static/' + node + "></td>"
        else:
            subcollection = listdir(join(path, node))
            subcollection.sort()
            for subnode in subcollection:
                site += "<td><img width=160 height=120 src=" + '/static/' + node + "/" + subnode + "><td>"
        i+=1
    site += "</tr>"
    site += "</table></body></html>"
    return site


@app.route('/receive_frame', methods=['POST'])
def handlePost():
    if request.method == 'POST':
        file = request.files['file']
        name = request.files['name']

        path = '/home/piotr/PycharmProjects/untitled3/static/'
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), 1)
        cv2.imwrite(path+name.read().decode(), img)
        return ""


if (__name__ == '__main__'):
    app.run(host='0.0.0.0')
