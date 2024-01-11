#----------------------------------------LOCAL - API

from flask import Flask, request
from flask_cors import CORS, cross_origin

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import datetime
dt = datetime.datetime.today()
date=str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)


client = MongoClient('localhost', 27017)
db = client.projectKHKTandSFTandTHT
auth = db.Auth
student = db.Student

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/api/register",methods=["POST"])
@cross_origin()
def Register():
    try:
        data = request.get_json(force=True)
        x = auth.insert_one(data)
        return str(x.inserted_id)
    except:
        return "error"


@app.route("/api/addnewstudent",methods=["POST"])
@cross_origin()
def addNewStudent():
    try:
        data = request.get_json(force=True)
        x = student.insert_one(data)
        return str(x.inserted_id)
    except:
        return "error"

if __name__ == "__main__":
    app.run(host="0.0.0.0")