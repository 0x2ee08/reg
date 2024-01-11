import cv2
import numpy as np
import sqlite3
import os
from checkMask import *
import json

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import time

client = MongoClient('localhost', 27017)

db = client.projectKHKTandSFTandTHT
student=db.Student

import datetime
dt = datetime.datetime.today()
date=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)

now = datetime.datetime.now()

import thanNhiet
import gmail
import drawData


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

    #im =cv2.imread()
paths='./xuLyAnh'
conn=sqlite3.connect("acess.db")

while 1:
    time.sleep(0.25)
    if(int(now.hour)==8):
        break
    imagePaths = [os.path.join(paths,f) for f in os.listdir(paths)]

    for path in imagePaths:
        try:
            im=cv2.imread(path)
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            Id, conf = recognizer.predict(gray)
            per=round(100-conf,2)
            cv2.imshow("Image", gray)
            cv2.waitKey(1)
            if per>40:
                query="SELECT * FROM idAndKey WHERE id =="+str(Id)
                c=conn.execute(query)
                for r in c:
                    key=r[1]
            
                checkm=check(path)
                mask_per=round(float(checkm[0][0])*100,2)

                temp=path.split('.')[2]
                temp=float(temp.replace('a','.'))

                mongo_query={"_id":ObjectId(key)}
                info=student.find_one(mongo_query)

                try:
                    info[date]["diemDanh"]="1"
                except:
                    info[date] = {"diemDanh":"1"}

                try:
                    flags=int(info[date]['thanNhietCao'])
                except:
                    flags=0
                

                try:
                    flag=int(info[date]['thanNhietBatThuong'])
                except:
                    flag=0


                if(temp>37.5 and not(flags)):
                    gmail.sendGmailTemp(info['tenHocSinh'],info['lopHocSinh'],"co than nhiet cao")
                    info[date]["thanNhietCao"]="1"

                if(thanNhiet.comThanNhiet(info['_id'],temp) and temp>35 and (not flag)):
                    gmail.sendGmailBatThuong(info['tenHocSinh'],info['lopHocSinh'],"co than nhiet bat thuong")
                    info[date]['thanNhietBatThuong']="1"

                #key_ref=ref.child(key)
                

                #date_ref=key_ref.child(date)

                if mask_per>90:
                    #student.update_one(mongo_query,{"$set":{date:{"diemDanh":"1","khauTrang":"0"}}})
                    info[date]["khauTrang"]="0"
                else:
                    info[date]["khauTrang"]="1"
                
                if(temp>34):
                    info[date]["thanNhiet"]=temp                      
                print(info)
                print(Id,per,'%',temp,key,checkm)
                print("---------------")
                student.update_one(mongo_query,{"$set":info})
        #     print(Id,per)
            os.remove(path)
        except:
            try:
                os.remove(path)
            except:
                pass
            cv2.waitKey(1)
cv2.destroyAllWindows()

for i in range(1,8):
    for j in range(6,10):
        lop=str(j)+"A"+str(i)
        gmail.guiDanhSachProcess(lop)
        drawData.drawL(lop)
        gmail.gmailFile(lop)
gmail.sendGmailPersonal()