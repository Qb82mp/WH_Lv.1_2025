from dotenv import load_dotenv
from mysql.connector import errorcode
import os
import mysql.connector


def getConnection():
    load_dotenv()
    try:
        config = {
            'user':  str(os.getenv('API_SQL_USER')),
            'password': str(os.getenv('API_SQL_PW')),
            'host': str(os.getenv('API_SQL_HOST')),
            'database': 'website',
            # 'raise_on_warnings': True
        }

        connectDB = mysql.connector.connect(**config)
        #print("連線成功")
        return connectDB
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("使用者名稱或密碼有誤，請確認並重新連線，謝謝。")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("請確認使用的database是否存在。")


def checkEmailIsDuplicate(item):
    _result = None
    cnx = getConnection()
    cursor = cnx.cursor()
    #print("1")
    try:
        #print("2")
        selectEmail = """SELECT email FROM member WHERE LOWER(email) = LOWER(%s);"""
        data = item.email
        cursor.execute(selectEmail, (data,))
        emailData = cursor.fetchall()
        if emailData != []:
            _result = True
            #print("有重複")

        if _result != True:
            # 將值儲存進資料庫中
            add_member = ("INSERT INTO member (name, email, password)"
                            "VALUES (%s, %s, %s)")
            data = (item.name, item.email, item.password)
            cursor.execute(add_member, data)
            #print("寫入")
            _result= False
    finally:
        if _result is not None:
            if _result != True:
                cnx.commit()
        if cursor is not None:
            cursor.close()
        if cnx is not None:
            cnx.close()
    
        return _result
    
def checkUserInfo(loginInfo):
    _result = {"0":None}
    cnx = getConnection()
    cursor = cnx.cursor()
    try:
        login_member = ("SELECT id, name, email, password FROM member WHERE email = %s AND password = %s")
        loginInput = (loginInfo.userEmail, loginInfo.pw)
        cursor.execute(login_member, loginInput)
        emailData = cursor.fetchone()
        if emailData != None:
            _result = {"0":True, "1":emailData[1], "2":emailData[0]}
            #print("找到")

        if _result["0"] != True:
            _result= {"0": False}
            #print("沒找到")
    finally:
        if _result is not None:
            if _result != True:
                cnx.commit()
        if cursor is not None:
            cursor.close()
        if cnx is not None:
            cnx.close()
    
        return _result

def saveComment(commInfo):
    _result = False
    cnx = getConnection()
    cursor = cnx.cursor()
    try:
        # 寫入
        insertComm = ("INSERT INTO message (member_id, content)"
                        "VALUES (%s, %s)")
        insertData = (commInfo["userid"], commInfo["comment"])
        cursor.execute(insertComm, insertData)
        #print("寫入訊息")
        _result = True
    finally:
        if _result == True:
            cnx.commit()
        if cursor is not None:
            cursor.close()
        if cnx is not None:
            cnx.close()
    
    if _result == True:
        return "完成寫入"
    else:
        return "未寫入完成"
    
def getComment(userId):
    _result={}
    cnx = getConnection()
    cursor = cnx.cursor()
    try:
        cursor.execute("SELECT memb.id AS memb_id, memb.name AS name, msg.id AS msg_id ,msg.content AS content FROM message AS msg INNER JOIN member AS memb ON memb.id = msg.member_id ORDER BY msg.time DESC")
        commData = cursor.fetchall()
        i = 0
        id = ""
        for memb_id, name, msg_id, content, in commData:
            if memb_id == userId:
                id = memb_id
            else:
                id = ""
            _result[i] = {"membId": id, "name": name, "content": content, "msg_id": msg_id}
            i +=1

    finally:
        if cursor is not None:
            cursor.close()
        if cnx is not None:
            cnx.close()

    return _result  

def delComment(commId):
    _result = False
    cnx = getConnection()
    cursor = cnx.cursor()
    try:
        cursor.execute("DELETE FROM message WHERE id = %s", (commId,))
        delRow = cursor.rowcount
        if delRow > 0:
            _result = True
            #print("刪除")
    finally:
        if _result == True:
            cnx.commit()
        else:
            cnx.rollback()
        if cursor is not None:
            cursor.close()
        if cnx is not None:  
            cnx.close()
    
    return _result