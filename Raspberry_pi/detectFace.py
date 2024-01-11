import cv2
import mediapipe as mp
import time
import json
import sqlite3
import sync_to_server

import socket
import tqdm
import os

import requests

from scipy import ndimage

import datetime
dt = datetime.datetime.today()
date=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)

import serial
try:
    try:
        ser = serial.Serial('/dev/ttyUSB0',9600)
    except:
        ser = serial.Serial('/dev/ttyUSB1',9600)
except:
    print("khong ket noi duoc voi man lcd")


import board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
frame = np.zeros((24*32,))

cap = cv2.VideoCapture(0)
pTime = 0

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')

conn=sqlite3.connect("acess.db")

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.75)
i=0
while True:
    mlx.getFrame(frame)
    data_array = np.fliplr(np.reshape(frame,(24,32)))
    data_array = ndimage.zoom(data_array,10)
    
   # obj_temp=np.amax(frame)
#     obj_temp=mlx.object_temperature
    obj_temp=round(np.amin(frame),1)
    obj_temp=str(obj_temp)
    obj_temp=obj_temp.replace('.','a')
    #print(obj_temp)
    
    success, img = cap.read()
    
    resize_img = cv2.resize(img, dsize=(320, 240))
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    # print(results)

    if results.detections:
        for id, detection in enumerate(results.detections):
            
            # mpDraw.draw_detection(img, detection)
            # print(id, detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)

            x=int(bboxC.xmin * iw)
            y=int(bboxC.ymin * ih)
            w=int(bboxC.width * iw)
            h=int(bboxC.height * ih)
            crop_img = img[y-50:y+h+20, x-20:x+w+20]
            
            num=2.12719298246
            rx=int((x+14)/num)
            ry=int((y+14)/num)
            rxw=int((x+w+14)/num)
            ryh=int((14+y+h)/num)
            cv2.rectangle(resize_img, (rx,ry),(rxw,ryh), (255, 0, 255), 2)
            mpx=int((x+w/2+14)/num)
            mpy=int((y+h/2+14)/num)
            
            try:
                obj_temp=round(data_array[mpx][mpy],1)
                obj_temp=str(obj_temp)
                obj_temp=obj_temp.replace('.','a')
            except:
                obj_temp="37a00"
            
            a=obj_temp.split("a")
            ot=a[0]+"."+a[1]
            
            resize_img = cv2.circle(resize_img, (mpx,mpy), 1, (255,0,0), 2)
            cv2.putText(resize_img, obj_temp,
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)

            
            if float(ot) >37.5:
                try:
                    ser.write((obj_temp.split("a")[0]+"."+obj_temp.split("a")[1]+"          Nhiet do cao"+"\n").encode())
                except: pass
            else:
                ser.write((obj_temp.split("a")[0]+"."+obj_temp.split("a")[1]+"\n").encode())

            try:
                filename = 'xuLyAnh/check'+str(i)+'.'+obj_temp+'.jpg'
                SEPARATOR = "<SEPARATOR>"
                BUFFER_SIZE = 4096

                cv2.imwrite(filename,crop_img)

                filesize = os.path.getsize(filename)
                s = socket.socket()
                s.connect(("192.168.0.104", 5001))
                s.send(f"{filename}{SEPARATOR}{filesize}".encode())

                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(filename, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        s.sendall(bytes_read)
                        progress.update(len(bytes_read))
                i+=1
                if(i==1000):
                    i=1
            except:
                pass
            cv2.rectangle(img, (x-20,y-50),(x+w+20,y+h+20), (255, 0, 255), 2)
            
            cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)

    else:
        ser.write((obj_temp.split("a")[0]+"."+obj_temp.split("a")[1]+"\n").encode())

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 255, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)