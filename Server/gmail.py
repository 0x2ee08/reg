import os
from datetime import date
from datetime import datetime
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)

db = client.projectKHKTandSFTandTHT
student=db.Student

from excel import *
from drawData import *
import json

import datetime
dt = datetime.datetime.today()
date=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)

def sendGmailPersonal():
    info=student.find()
    for person in info:
        toaddr=info["gmailHocSinh"]
        fromaddr = "projectkttl.ts.ntl.2020@gmail.com"
        #toaddr = "thuyduong0754@gmail.com, giabaok8@outlook.com, lekhoavu2008@gmail.com, nhatlongcute2340@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Bảng thống kê thân nhiệt học sinh "+list_ref[key]['tenHocSinh']
        body = "Bảng thống kê thân nhiệt học sinh "+list_ref[key]['tenHocSinh']+"\n"

        msg.attach(MIMEText(body, 'plain'))

        #edit file nảme thành excel
        All_filename = "./thanNhietTable/All/"+list_ref[key]['lopHocSinh']+"/"+list_ref[key]['tenHocSinh']+".png"
        Daily_filename="./thanNhietTable/Daily/"+list_ref[key]['lopHocSinh']+"/"+list_ref[key]['tenHocSinh']+".png"

        try:
            All_attachment = open(All_filename, "rb")
        except:
            All_attachment = open('./thanNhietTable/Vang.jpeg', "rb")

        try:
            Daily_attachment=open(Daily_filename,"rb")
        except:
            Daily_attachment=open('./thanNhietTable/Vang.jpeg',"rb")


        part = MIMEBase('application', 'octet-stream')
        part.set_payload((All_attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % "All")
        msg.attach(part)

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((Daily_attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % "Daily")
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "giabao7727")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr.split(","), text)
        server.quit()

def gmail(tenHocSinh,lopHocSinh,warn):
    fromaddr = "projectkttl.ts.ntl.2020@gmail.com"
    toaddr=""

    info=student.find()
    for person in info:
        if(info["lopHocSinh"]=="admin"or info["lopHocSinh"] == "GV" or info["tenHocSinh"] == tenHocSinh):
            toaddr+=(info["gmailHocSinh"]+",")
    toaddr+="giabaok8@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Hoc sinh "+tenHocSinh+" lop "+lopHocSinh+" "+warn
    body = "Hoc sinh "+tenHocSinh+" lop "+lopHocSinh+" "+warn
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "giabao7727")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr.split(","), text)
    server.quit()

def gmailFile(lopHocSinh):
    try:
        toaddr=""
        
        info=student.find()
        for person in info:
            if(info["lopHocSinh"]=="admin"or info["lopHocSinh"] == "GV" or info["lopHocSinh"] == lopHocSinh):
                toaddr+=(info["gmailHocSinh"]+",")
        toaddr+="giabaok8@outlook.com"

        fromaddr = "projectkttl.ts.ntl.2020@gmail.com"
        #toaddr = "thuyduong0754@gmail.com, giabaok8@outlook.com, lekhoavu2008@gmail.com, nhatlongcute2340@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Danh sach diem danh lop"+lopHocSinh
        body = "Danh sach diem danh \n"

        msg.attach(MIMEText(body, 'plain'))

        #edit file nảme thành excel
        filename = "./diemDanh/"+lopHocSinh+"/"+date+".xlsx"

        attachment = open(filename, "rb")


        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % lopHocSinh+" "+date)
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "giabao7727")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr.split(","), text)
        server.quit()
    except:
        pass

def sendGmailTemp(tenHocSinh,lopHocSinh):
    #ser.write("|| Gui gmail nhiet do tren 38 do ||".encode())
    gmail(tenHocSinh,lopHocSinh,"co nhiet do tren 38 oC")

def sendGmailBatThuong(tenHocSinh,lopHocSinh):
    #ser.write("|| Gui gmail nhiet do bat thuong ||".encode())
    gmail(tenHocSinh,lopHocSinh,"co nhiet do bat thuong")

def guiDanhSachProcess(lopHocSinh):
    i=1
    info=student.find()
    for person in info:
        if person["lopHocSinh"]==lopHocSinh:
            if(i==1):
                i=str(i)
                try:
                    updateDL('./diemDanh/'+lopHocSinh+"/"+date+".xlsx",'A'+i,'B'+i,'C'+i,'D'+i,'E'+i,'Ten hoc sinh','Lop hoc sinh','Diem danh','Than nhiet trung binh','Khau trang')
                except:
                    os.makedirs('./diemDanh/'+lopHocSinh)
                i=int(i)+1
            i=str(i)
            try:
                thanNhiet=0
                try:
                    thanNhiet=float(person[date]["thanNhiet"])
                except:
                    pass
                if(thanNhiet==0):
                    updateDL('./diemDanh/'+lopHocSinh+"/"+date+".xlsx",'A'+i,'B'+i,'C'+i,'D'+i,'E'+i,person['tenHocSinh'],person['lopHocSinh'],'Co','Chua do',person[date]['khauTrang'])
                else:
                    if(person['khauTrang']=="0"):
                        khauTrang="Khong"
                    else:
                        khauTrang="Co"
                    updateDL('./diemDanh/'+lopHocSinh+"/"+date+".xlsx",'A'+i,'B'+i,'C'+i,'D'+i,'E'+i,person['tenHocSinh'],person['lopHocSinh'],'Co',str(thanNhiet),khauTrang)
            except:
                updateDL('./diemDanh/'+lopHocSinh+"/"+date+".xlsx",'A'+i,'B'+i,'C'+i,'D'+i,'E'+i,person['tenHocSinh'],person['lopHocSinh'],'Vang','Vang','Vang')
            i=int(i)+1