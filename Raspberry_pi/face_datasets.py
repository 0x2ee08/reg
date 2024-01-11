import cv2
import numpy as np
import sqlite3
import mediapipe as mp
import os
import time

import json

import requests


def insertGetID(tenHocSinh,lopHocSinh,gmailHocSinh):
    # Tạo tk trên db
    auth={"email":gmailHocSinh,"password":"25d55ad283aa400af464c76d713c07ad"}
    data={'tenHocSinh':tenHocSinh,'lopHocSinh':lopHocSinh,'gmailHocSinh':gmailHocSinh}
    a = requests.post("http://192.168.0.104:5000/api/register",json=auth)
    response= requests.post("http://192.168.0.104:5000/api/addnewstudent",json=data) 

    key=response.text
    conn=sqlite3.connect("./acess.db")
    query="INSERT INTO idAndKey(key) VALUES('"+key+"')"
    c=conn.execute(query)
    conn.commit()
    query="SELECT * FROM idAndKey WHERE key=='"+key+"'"
    c=conn.execute(query)
    for r in c:
        new_key=r[0]
    print(new_key)
    return int(new_key)


def getFace(face_id,count):
    i=count
    while True:
        success, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

                try:
                    cv2.imwrite("dataset/"+"User." + str(face_id) + '.' + str(count) + ".jpg", gray[y-50:y+h+20,x-20:x+w+20])
                    count+=1

                    cv2.rectangle(img, (x,y),(x+w,y+h), (255, 0, 255), 2)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                                (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
                except:
                    pass
        name="Lay DL"
        cv2.namedWindow(name)        
        cv2.moveWindow(name, 280,230)
        cv2.imshow(name, img)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        elif count>i+100:

            cv2.destroyAllWindows()
            break

while True:
    cap = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    quit=input("press q to quit:")
    if quit=="q":
        break
    else:
        pass
    tenHocSinh=input("Nhap ten:")
    lopHocSinh=input("Nhap lop:")
    gmailHocSinh=input("Nhap gmail:")
    face_id=insertGetID(tenHocSinh,lopHocSinh,gmailHocSinh)

    mpFaceDetection = mp.solutions.face_detection
    mpDraw = mp.solutions.drawing_utils
    faceDetection = mpFaceDetection.FaceDetection(0.75)

    print("Hay thao khau trang (neu co)")
    input("Enter de tiep tuc")
    getFace(face_id,0)
    print("-------------")
    print("Hay deo khau trang")
    input("Enter de tiep tuc")
    getFace(face_id,101)
    cap.release()
    print("-------------")
