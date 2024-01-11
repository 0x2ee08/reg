import requests
import sqlite3
import pyrebase
import os
import mediapipe as mp
import cv2
import json

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.75)

print("Uploading data to storage...")
response = requests.get("http://e56a-42-114-118-50.ngrok.io/api/send_data_to_storage")
print("Uploaded.")

print("Downloading data...")

paths = "./storage"
imagePaths = [os.path.join(paths, f) for f in os.listdir(paths)]

for file in imagePaths:
    _name=file.split('.')

    flag=0
    conn=sqlite3.connect("./acess.db")
    key=(_name[1].split("/"))[2]
    query="SELECT * FROM idAndKey WHERE key=='"+key+"'"
    c=conn.execute(query)
    for r in c:
        flag=1
    if flag==0:
        #create account with id

        query="INSERT INTO idAndKey(key) VALUES('"+key+"')"
        c=conn.execute(query)
        conn.commit()
        query="SELECT * FROM idAndKey WHERE key=='"+key+"'"
        c=conn.execute(query)
        for r in c:
            new_key=r[0]
        path = "./storage"
        imagePath = [os.path.join(paths, f) for f in os.listdir(paths)]

        os.rename(file, "./download_img/User."+str(new_key)+"."+str((file.split('.'))[2])+".jpg")
            #names=(file.name).split('/')
            #if(names[0]==key):
                #st.download(files.name,"download_img/User."+str(new_key)+"."+str((names[1].split('.'))[0])+".jpg",user['idToken'])
    else:
        query="SELECT * FROM idAndKey WHERE key=='"+key+"'"
        c=conn.execute(query)
        for r in c:
            new_key=r[0]
        path = "./storage"
        imagePath = [os.path.join(paths, f) for f in os.listdir(paths)]

        os.rename(file, "./download_img/User."+str(new_key)+"."+str((file.split('.'))[2])+".jpg")

        

print("Downloaded.")

print("Xu ly data...")

paths="./download_img"

imagePaths = [os.path.join(paths,f) for f in os.listdir(paths)]

for path in imagePaths:
    img=cv2.imread(path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                int(bboxC.width * iw), int(bboxC.height * ih)

            x=int(bboxC.xmin * iw)
            y=int(bboxC.ymin * ih)
            w=int(bboxC.width * iw)
            h=int(bboxC.height * ih)

            cv2.imwrite(path, gray[y-50:y+h+20,x-20:x+w+20])
    file_arr=path.split("/")
    new_path=file_arr[0]+"/"+"dataset"+"/"+file_arr[2]
    os.rename(path, new_path)

print("Done")