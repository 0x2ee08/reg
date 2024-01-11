import os
#import sqlite3
from datetime import date
from xuLyDBThanNhiet import *
import gmail

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)

db = client.projectKHKTandSFTandTHT
student=db.Student

import json

def getAverageThanNhiet(_id):
    arr=[]

    mongo_query={"_id":ObjectId(_id)}
    info=student.find_one(mongo_query)

    for key, value in info.items():
        if(key!="_id" and key!="tenHocSinh" and key!="lopHocSinh" and key!="gmailHocSinh"):
            for date, temp in value.items():
                if(date=="thanNhiet"):
                    arr.append(float(temp))
    (ul,ll)=checkOutlierV2(arr)
    return (ul,ll)
    
    
    

def comThanNhiet(_id,thanNhiet):
    (ul,ll) = getAverageThanNhiet(_id)
    if (thanNhiet>ul or thanNhiet<ll):
        return 1
    return 0
