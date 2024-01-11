from flask import Flask, redirect, url_for, render_template, request, make_response
from flask_cors import CORS, cross_origin
import jwt
from functools import wraps
import hashlib

import socket
import tqdm
import os
import json
import pickle
import urllib

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

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
app.config["SECRET_KEY"]="DemoSecretKeyProjectTHTSFTKHKT"
app.config["NGROK_URL"]="https://236c-113-22-175-181.ngrok.io/"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.cookies.get("token")

        try:
            data=jwt.decode(token,app.config["SECRET_KEY"], algorithms="HS256")
        except:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrap

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def post_login():
    if request.form["button"] == "Đăng nhập":
        gmail = request.form["gmail"]
        password = request.form["pass"]
        hash_pass = (hashlib.md5(password.encode())).hexdigest()
        try:
            user=auth.find_one({"email":gmail})
            if user["password"] == hash_pass:
                token= jwt.encode({"email":user["email"],"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=15)},app.config["SECRET_KEY"])
                resp = make_response(redirect("/main"))
                resp.set_cookie("token", token)
                return resp
            else:
                return redirect("/login")
        except:
            return redirect("/login")
    else:
        return redirect("/register")

@app.route("/register")
def registerPage():
    resp = make_response(render_template("register.html"))
    resp.set_cookie("token", "")
    return resp

@app.route("/register", methods=["POST"])
def returnLogin():
    return redirect("/login")

@app.route("/main")
@login_required
def main():
    token = request.cookies.get("token")
    data=jwt.decode(token,app.config["SECRET_KEY"], algorithms="HS256")
    if data["email"] == "bot.projectthtandkttl@gmail.com":
        return render_template("admin.html")
    info = student.find_one({"gmailHocSinh":data["email"]})
    try:
        if str(info[date]["khauTrang"])=="1":
            khauTrang="Co"
        else:
            khauTrang="Khong"
        try:
            info[date]["thanNhietCao"]
            tnc="Hoc Sinh co than nhiet tren 37.5"
        except:
            tnc="Khong"
        try:
            info[date]["thanNhietBatThuong"]
            tnbt="Hoc sinh co than nhiet bat thuong"
        except:
            tnbt="Khong"
        return render_template("index.html",day=date,gmail=data["email"],name=info['tenHocSinh'],lop=info["lopHocSinh"],diemDanh="Co",khauTrang=khauTrang,thanNhiet=info[date]["thanNhiet"],tnc=tnc,tnbt=tnbt)
    except:
        return render_template("index.html",day=date,gmail=data["email"],name=info['tenHocSinh'],lop=info["lopHocSinh"],diemDanh="N/A",khauTrang="N/A",thanNhiet="N/A",tnc="N/A",tnbt="N/A")

@app.route("/main", methods=["POST"])
@login_required
def mainProcess():
    if request.form["button"] == "Đăng xuất":
        resp = make_response(redirect("/login"))
        resp.set_cookie("token", "")
        return resp
    elif request.form["button"] == "Tìm thông tin":
        day = request.form["day"]
        day = day.split("-")
        try:
            key = day[0]
            day[0] = day[2]
            day[2] = key
            find_date = (str(int(day[0])) + "-" + str(int(day[1])) + "-" + str(int(day[2])))
        except:
            find_date = ""
        token = request.cookies.get("token")
        data=jwt.decode(token,app.config["SECRET_KEY"], algorithms="HS256")
        info = student.find_one({"gmailHocSinh":data["email"]})
        try:
            if str(info[find_date]["khauTrang"])=="1":
                khauTrang="Co"
            else:
                khauTrang="Khong"
            try:
                info[find_date]["thanNhietCao"]
                tnc="Hoc Sinh co than nhiet tren 37.5"
            except:
                tnc="Khong"
            try:
                info[find_date]["thanNhietBatThuong"]
                tnbt="Hoc sinh co than nhiet bat thuong"
            except:
                tnbt="Khong"
            return render_template("index.html",day=find_date,gmail=data["email"],name=info['tenHocSinh'],lop=info["lopHocSinh"],diemDanh="Co",khauTrang=khauTrang,thanNhiet=info[find_date]["thanNhiet"],tnc=tnc,tnbt=tnbt)
        except:
            return render_template("index.html",day=find_date,gmail=data["email"],name=info['tenHocSinh'],lop=info["lopHocSinh"],diemDanh="N/A",khauTrang="N/A",thanNhiet="N/A",tnc="N/A",tnbt="N/A")

    elif request.form["button"] == "Đổi mật khẩu":
        token = request.cookies.get("token")
        data=jwt.decode(token,app.config["SECRET_KEY"], algorithms="HS256")
        info = student.find_one({"gmailHocSinh":data["email"]})

        reset_token= jwt.encode({"email":data["email"],"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=5)},app.config["SECRET_KEY"])

        fromaddr = "projectkttl.ts.ntl.2020@gmail.com"
        toaddr=data["email"]

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Reset Pass"
        body =" Click here : " + app.config["NGROK_URL"]+ 'resetPass/'+token
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "giabao7727")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr.split(","), text)
        server.quit()

        resp = make_response(redirect("/login"))
        resp.set_cookie("token", "")
        return resp
    elif request.form["button"] == "Tạo mã":
        try:
            token = request.cookies.get("token")
            data=jwt.decode(token,app.config["SECRET_KEY"], algorithms="HS256")
        except:
            return redirect("/login")

        try:
            if data["email"] == "bot.projectthtandkttl@gmail.com":
                _choice = request.form["get_info_choice"]
                _name = request.form["name"]
                _class = request.form["class"]
                _email = request.form["email"]
                if _choice == "Hoc Sinh":
                    datas = {
                        "tenHocSinh": _name,
                        "lopHocSinh": _class,
                        "gmailHocSinh": _email,
                    }
                else:
                    datas = {
                        "tenHocSinh": _name,
                        "lopHocSinh": "GV",
                        "gmailHocSinh": _email,
                    }
                x = student.insert_one(datas)

                return render_template("admin.html", key=x.inserted_id)
            else:
                return redirect("login")
        except:
            return redirect("login")

@app.route("/resetPass/<token>")
def resetPass(token):
    try:
        data=jwt.decode(token,app.config["SECRET_KEY"], algorithms="HS256")
        return render_template("reset.html")
    except:
        return redirect("/login")

@app.route("/resetPass/<token>", methods=["POST"])
def post_resetPass(token):
    try:
        data=jwt.decode(token,app.config["SECRET_KEY"], algorithms="HS256")
        password = request.form["password"]
        re_enter_password = request.form["re_enter_password"]

        if(password == re_enter_password):
            hash_pass = (hashlib.md5(password.encode())).hexdigest()
            auth.update_one({"email":data["email"]},{"$set":{"email":data["email"],"password":hash_pass}})
            return redirect("/login")
        else:
            return render_template("reset.html")
    except:
        return redirect("/login")

@app.route("/")
def index():
    return redirect("/main")


#-------------------------------------- PUBLIC - API
@app.route("/api")
@cross_origin()
def test():
    return "Hello, Public API works !!! :D"


@app.route("/api/dang_nhap", methods=["POST"])
@cross_origin()
def sign_in():
    gmailAndPass = request.get_json(force=True)
    try:
        hash_pass = (hashlib.md5(gmailAndPass["pass"].encode())).hexdigest()
        user=auth.find_one({"email":gmailAndPass["gmail"]})
        if user["password"] == hash_pass:
            token= jwt.encode({"email":user["email"],"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=5)},app.config["SECRET_KEY"])
        return token
    except:
        return "error"


@app.route("/api/get_all_info", methods=["POST"])
@cross_origin()
def get_all_info():
    try:
        try:
            token = request.get_json(force=True)
            data=jwt.decode(token["token"],app.config["SECRET_KEY"], algorithms="HS256")
            all_info = student.find_one({"gmailHocSinh":data["email"]})
            all_info["_id"]=""
            all_info=json.dumps(all_info)
            return all_info
        except:
            return "error"
    except:
        return "error"

@app.route("/api/check_uid", methods=["POST"])
@cross_origin()
def check_uid():
    try:
        ids = request.get_json(force=True)
        info=student.find_one({"_id":ObjectId(ids["uid"])})
        if(info==None):
            return "false"
        return "true"
    except:
        return "false"

@app.route("/api/upload_image_uri", methods=["POST"])
@cross_origin()
def upload_image_uri():
    try:
        data = request.get_json(force=True)
        file = open("img_user_data/" + data["uid"] + ".txt", "wb")
        pickle.dump(data, file)
        file.close()
        return "success"
    except:
        return "error"


@app.route("/api/send_data_to_storage")
@cross_origin()
def send_data_to_storage():
    #try:
        paths = "./img_user_data"
        imagePaths = [os.path.join(paths, f) for f in os.listdir(paths)]
        for path in imagePaths:
            file = open(path, "rb")
            data = pickle.load(file)
            file.close()

            for i in range(201):
                uri_link = "uri" + str(i)
                image_url = data[uri_link]
                save_name = "./storage/"+data["uid"] +"."+ str(i) + ".jpg"  # local name to be saved
                urllib.request.urlretrieve(image_url, save_name)

                filename=save_name
                filesize = os.path.getsize(filename)
                s = socket.socket()
                s.connect(("192.168.0.105", 5001))
                s.send(f"{filename}{SEPARATOR}{filesize}".encode())

                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(filename, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        s.sendall(bytes_read)
                        progress.update(len(bytes_read))
                s.close()

                os.remove(save_name)
        return "success"
    #except:
        #return "error"


@app.errorhandler(404)
def error(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
    # serve(app, host='0.0.0.0', port=8080, threads=1)