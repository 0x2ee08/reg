#import sqlite3

import pyrebase
firebaseConfig = {
    'apiKey': "AIzaSyB52z4UCsZA9Xmp8eUSviVFfhpMyaa0J8M",
    'authDomain': "projectthtandkttl.firebaseapp.com",
    'databaseURL':"",
    'projectId': "projectthtandkttl",
    'storageBucket': "projectthtandkttl.appspot.com",
    'messagingSenderId': "909774809704",
    'appId': "1:909774809704:web:a75da0caef487a4624e9dd",
    'measurementId': "G-5JM3EGSKBK"
}

firebase=pyrebase.initialize_app(firebaseConfig)

def insertOrUpdate(idHocSinh,diemDanh,thanNhiet,khauTrang):
    conn = sqlite3.connect('/home/pi/Desktop/Nas_db/dbHocSinh.db')

    query="SELECT*FROM hocSinh WHERE idHocSinh="+str(idHocSinh)
    cusror = conn.execute(query)

    isRecordExist =0 
    for row in cusror:
        isRecordExist=1
    query="UPDATE hocSinh SET diemDanh='"+str(diemDanh)+"' WHERE idHocSinh="+str(idHocSinh)
    conn.execute(query)
    conn.commit()
    
    query="UPDATE hocSinh SET khauTrang='"+str(khauTrang)+"' WHERE idHocSinh="+str(idHocSinh)
    conn.execute(query)
    conn.commit()
    
    query="UPDATE hocSinh SET thanNhiet='"+str(thanNhiet)+"' WHERE idHocSinh="+str(idHocSinh)
    conn.execute(query)
    conn.commit()
    
    conn.close()

def getProfile(idHocSinh):

    conn = sqlite3.connect('/home/pi/Desktop/Nas_db/dbHocSinh.db')
    query="SELECT*FROM hocSinh WHERE idHocSinh="+str(idHocSinh)
    cusror = conn.execute(query)

    profile=None 
    for row in cusror:
        profile=row
    conn.close()
    return profile
