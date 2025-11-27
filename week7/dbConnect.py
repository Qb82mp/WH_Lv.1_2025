from mysql.connector.aio import connect
from dotenv import load_dotenv
import os

async def connectDB():
    load_dotenv()
    config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": os.getenv("API_SQL_Password"),
        "port": 3306,
        "database": "website",
    }

    connDatabase = None
    try:
        # 使用**config，等同於host="127.0.0.1", user="root", password="xxxxx"。
        connDatabase = await connect(**config)
        #print("連線成功")
    except Exception as e:
        print("連線資料庫出現錯誤。")

    return connDatabase


async def checkEmail(item):
    _result = False
    #print("1")
    cnx = await connectDB()
    cursor = await cnx.cursor()
    try:
        # 檢查email是否有重複
        queryEmail = """SELECT email FROM member WHERE LOWER(email)=LOWER(%s);"""
        paraStr = item.email
        await cursor.execute(queryEmail, (paraStr,))
        findData = await cursor.fetchone()
        #print("2")
        if findData != None:
            _result = True
            #print("重複信箱")

        
        # 沒有重複就執行註冊動作
        if _result != True:
            signUpInfo = """INNERT INTO member (name, email, password) VALUES(%s, %s, %s)"""
            await cursor.exxcute(signUpInfo, (item.name, item.email, item.pw,))
            #print("註冊完成")
    finally:
        if _result != True:
            await cursor.commit()
        if cursor is not None:
            await cursor.close()
        if cnx is not None:
            await cnx.close()

        return _result

async def checkMemberInfo(item):
    _result = {1:False}
    cnx = await connectDB()
    cursor = await cnx.cursor()
    try:
        # 確認是否有此會員
        queryMemb = """SELECT id, name FROM member WHERE email=%s AND password=%s;"""
        paraMemb = (item.email, item.password)
        await cursor.execute(queryMemb, paraMemb)
        findData = await cursor.fetchone()
        if findData != None:
            _result = {1:True, 2:findData[1], 3:findData[0]}
        #print("有成功執行")
    finally:
        if cursor is not None:
            await cursor.close()
        if cnx is not None:
            await cnx.close()

        return _result

async def queryMemb(item):
    _result = None
    cnx = await connectDB()
    cursor = await cnx.cursor()
    try:    
        queryNum = """SELECT id, name, email FROM member WHERE id=%s;"""
        parameterStr = item.number
        await cursor.execute(queryNum, (parameterStr,))
        findData = await cursor.fetchone()

        if findData != None:
            _result = {
                    "id": findData[0],
                    "name": findData[1],
                    "email": findData[2]
                }
            
        if _result != None and findData != None:
            # 只儲存查詢別人的資料，不儲存自己查自己的資料
            if findData[0] != item.queryUser:
                #print("更新查詢")
                searchUser = """INSERT INTO search (be_queried_id, query_id) VALUES (%s, %s);"""
                paraUser = (findData[0], item.queryUser)
                await cursor.execute(searchUser, paraUser)
                await cnx.commit()
                #print("寫入查詢表中")
        #print("有成功執行")
    finally:
        if cursor is not None:
            await cursor.close()
        if cnx is not None:
            await cnx.close()

        return _result
    

async def updateMembName(item):
    _result = None
    cnx = await connectDB()
    cursor = await cnx.cursor()
    try:
        newName = item["newName"]
        oldName = item["oldName"]
        id = item["userId"]
        updateName = """UPDATE member SET name=%s WHERE name=%s AND id=%s;"""
        paraStr = (newName, oldName, id)
        #print("1")
        await cursor.execute(updateName, paraStr)
        await cnx.commit()

    except Exception as err:
        print("沒有更新成功")
    finally:    
        updateCount = cursor.rowcount
        if updateCount > 0:
            _result = {"ok": True}
        #     print("成功被更新")
        # else:
        #     print("沒有更新成功")
        
        if cursor is not None:
            await cursor.close()
        if cnx is not None:
            await cnx.close()

        return _result
    
async def queryMeMemb(item):
    _result = None
    cnx = await connectDB()
    cursor = await cnx.cursor()
    try:
        searchMe = """SELECT memb.name AS name, sear.time AS time FROM search AS sear INNER JOIN member AS memb ON sear.be_queried_id=%s AND sear.query_id=memb.id ORDER BY sear.time DESC LIMIT 10 OFFSET 0;"""
        paraStr = item["userId"]
        await cursor.execute(searchMe, (paraStr,))
        findData = await cursor.fetchall()

        if findData != {}:
            data = {}
            i = 0
            for name, time, in findData:
                membStr = name + " (" + str(time) + ")"
                keyStr = "dt"+str(i)
                data[keyStr] = membStr
                i+=1
            if data != {}:
                _result = data
    finally:
        if cursor is not None:
            await cursor.close()
        if cnx is not None:
            await cnx.close()

        return _result