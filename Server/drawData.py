import matplotlib.pyplot as plt
import datetime
#import sqlite3
import os

dt=datetime.datetime.today()

day=str(dt.day)+'-'+str(dt.month)+'-'+str(dt.year)


import json

def drawL(lopHocSinh):
    x=[]
    y=[]
    x1=[]
    y1=[]
    info=student.find()
    for person in info:
        if(person['lopHocSinh']==lopHocSinh):
            print('---Hom nay---'+person['tenHocSinh']+'---')
            try:
                temp=float(person[day]["thanNhiet"])
                y1.append(temp)
                x1.append(day)
            except:
                continue


            if info!="gmailHocSinh" and info!="lopHocSinh" and info!="tenHocSinh" and info!="_id":
                print('---Tat ca---'+person['tenHocSinh']+'---')

                try:
                    temp=float(person[day]['thanNhiet'])
                    y.append(temp)
                    x.append(info+" - "+lanDo)
                    print(info+" - "+lanDo)
                except:
                    continue

    
            fig, ax = plt.subplots(figsize=(len(x)*2, 6))

            ax.set(title = "Thân nhiệt học sinh",
            xlabel = "Ngày + lần đo thứ n", 
            ylabel = "Nhiệt độ (oC)")
            
            plt.plot(x,y,'go-')

            try:
                os.mkdir('./thanNhietTable/All/'+lopHocSinh)
            except:
                pass
            try:
                plt.savefig('./thanNhietTable/All/'+lopHocSinh+'/'+person['tenHocSinh']+'.png', bbox_inches='tight')
            except:
                print("Chưa có thông tin")

            
            fig, ax = plt.subplots(figsize=(len(x1)*2, 6))

            ax.set(title = "Thân nhiệt học sinh",
            xlabel = "Ngày + lần đo thứ n", 
            ylabel = "Nhiệt độ (oC)")
            
            plt.plot(x1,y1,'go-')

            try:
                os.mkdir('./thanNhietTable/Daily/'+lopHocSinh)
            except:
                pass
            try:
                plt.savefig('./thanNhietTable/Daily/'+lopHocSinh+'/'+person['tenHocSinh']+'.png', bbox_inches='tight')
            except:
                print("Chưa có thông tin")
    plt.clf()
