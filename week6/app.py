from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from dotenv import load_dotenv
import mysqlConnect
import os

load_dotenv()
middleware = [
    Middleware(SessionMiddleware,
               secret_key=os.getenv('API_KEY'),
               max_age=3600,
               https_only=True),
    Middleware(CORSMiddleware,
               allow_origins=["http://127.0.0.1:8000"],
               allow_credentials=True,
               allow_methods=[
                   "POST",
                   "GET"
                    ],
                allow_headers=["Content-Type"],
               )
]

app = FastAPI(middleware=middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="webPage")

@app.get("/", name="Home_Page")
def root(request: Request):
    return templates.TemplateResponse("memberSystem.html", {"request": request})


@app.get("/member")
def memberPage(request: Request):
    if request.session.get("name") != None:
        comment = mysqlConnect.getComment()
        context = {
            "request": request,
            "pageTitle": "歡迎光臨，這是會員頁",
            "name": request.session["name"]
        }
        if comment != {}:
            context["comments"] = comment
        return templates.TemplateResponse("memberSystem.html", context=context)
    else:
        return RedirectResponse(url="/", status_code=303)

@app.get("/ohoh")
def errorPage(msg: str,request: Request): # , errorMsg: str
    context = {
        "request": request,
        "pageTitle": "失敗頁面",
        "errInfo": msg
        # "errInfo": "帳號、或密碼輸入錯誤"
    }
    return templates.TemplateResponse("memberSystem.html", context=context)

class loginInfo(BaseModel):
    userEmail: str
    pw: str

@app.post("/login")
def logIn(userEmail: Annotated[str, Form()], pw: Annotated[str, Form()], request: Request):
    try:
        userInfo = loginInfo(userEmail=userEmail, pw=pw)
        result = mysqlConnect.checkUserInfo(userInfo)
        if result["0"] == True:
            request.session["name"] = result["1"]
            request.session["userId"] = result["2"]
            return RedirectResponse(url="/member", status_code=303)
        else:
            return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)
    except Exception as e:
        print("連線發生錯誤")

@app.get("/logout")
def logOut(request: Request):
    if request.session.get("name") != None:
        request.session.clear()

    return RedirectResponse(url="/", status_code=303)


# 在api取得要儲存進資料庫的json格式資料
class userInfo(BaseModel):
    name: str
    email: str
    password: str

@app.post("/signup")
def signUp(item: userInfo):
    try:
        result = mysqlConnect.checkEmailIsDuplicate(item)
        if result == True:
            # encode_msgValue = quote("重複的電子郵件")
            # url_str = f"/ohoh?msg={encode_msgValue}"
            return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)
        else:
            return RedirectResponse(url="/", status_code=303)
    except Exception as err:
        print("連線有錯誤", err)

class commentInfo(BaseModel):
    comment: str 

@app.post("/createMessage")
def inputMsg(comm: commentInfo, request: Request):
    try:
        msgInfo = {"comment": comm.comment,
                   "userid": request.session["userId"]}
        _resultMsg = mysqlConnect.saveComment(msgInfo)
        if _resultMsg == "完成寫入":
            return RedirectResponse(url="/member", status_code=303)  
    except Exception as err:
        print("連線有錯誤", err)

    
@app.post("/deleteMessage")
def delMsg(commId: Annotated[int, Form()]):
    try:
        _result = mysqlConnect.delComment(commId)
        if _result == True:
            return RedirectResponse(url="/member", status_code=303)
    except Exception as err:
        print("連線發生錯誤。")