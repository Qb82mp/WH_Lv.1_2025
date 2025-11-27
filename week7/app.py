from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import dbConnect
import os


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates= Jinja2Templates(directory="webPage")

load_dotenv()
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv('API_SECRET_KEY'),
                   max_age=1800,
                   https_only=True)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://127.0.0.1"],
                   allow_credentials=True,
                   allow_methods=[
                       "GET",
                       "POST",
                       "PATCH"
                        ],
                   allow_headers=["Content-Type"])


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="basePage.html")

@app.get('/ohoh')
async def errPage(msg: str, request:Request):
    content={
        "request":request,
        "errorMsg": msg
    }
    return templates.TemplateResponse(name="errorPage.html", context=content)

@app.get('/member')
async def member(request: Request):
    if request.session.get('name') != None and request.session.get('userid') != None:
        content = {
            "request": request,
            "info": {"name": request.session["name"]}
        }
        return templates.TemplateResponse(name="loggedPage.html", context=content)
    else:
        # 303為See Other，改用GET並根據location重新導向URL。
        return RedirectResponse(url='/', status_code=303)     

class logInfo(BaseModel):
     email: str
     password: str

@app.post('/login')
async def login(item: logInfo, request: Request):
    try:
        _result = await dbConnect.checkMemberInfo(item)
        if _result[1] == True:
            request.session["name"] = _result[2]
            request.session["userid"] = _result[3]
            
            return RedirectResponse(url='/member', status_code=303)
        else:
            return RedirectResponse(url='/ohoh?msg=電子郵件或密碼錯誤', status_code=303)
    except Exception:
        print("連線發生錯誤。")
        return RedirectResponse(url='ohoh?msg=連線發生錯誤', status_code=303)
        

class signUpInfo(BaseModel):
    name: str
    email: str
    pw: str

@app.post('/signup')
async def signUp(item: signUpInfo):
    try:
        _result = await dbConnect.checkEmail(item)
        if _result == True:
            return RedirectResponse(url='/ohoh?msg=重複的電子郵件', status_code=303)
        else:
            return RedirectResponse(url='/', status_code=303)
    except Exception:
        # if "422 Unprocessable Entity" in err:
        #     print("發生前端資料與後端資料格式不符，所發生的錯誤。") 
        # else:
            print("發生連線錯誤。")
            return RedirectResponse(url='ohoh?msg=連線發生錯誤')

@app.get('/logout')
async def logOut(request: Request):
    if request.session.get("name") != None and request.session.get("userid") != None:
        request.session.clear()
    
    return RedirectResponse(url='/', status_code=303)

class searchItem(BaseModel):
    number: int
    queryUser: int

@app.get('/api/member/{id}')
async def queryMember( id: int, request: Request):
    # 驗證使用者狀態
    if request.session.get("name") != None and request.session.get("userid"):
        item = searchItem(number = id, queryUser= request.session["userid"])
        try:
            _result = await dbConnect.queryMemb(item)
            if _result != None:
                
                content ={
                    "data": _result
                }
                # 要將資料以json格式傳送
                return JSONResponse(content)
        except Exception:
            print("連線發生錯誤")

    # 將資料轉為json格式，參數對應的值會由python的None轉為null。
    content ={"data": None}
    return JSONResponse(content)

class upDateName(BaseModel):
    name: str

@app.patch('/api/member')
async def upDateMemberName(item: upDateName, request:Request):
    if request.session.get("name") != None and request.session.get("userid"):
        _updateInfo = {
            "newName": item.name,
            "oldName": request.session["name"],
            "userId": request.session["userid"]
        }
        try:
            _result = await dbConnect.updateMembName(_updateInfo)
            if _result != None:
                request.session["name"] = item.name
                #print("更新成功")
                return JSONResponse(_result)

        except Exception:
            print("連線錯誤。")

    # 沒更新成功
    content = {"error": True}
    return JSONResponse(content)


@app.get('/api/search')
async def searchMe(request: Request):
    if request.session.get("name") != None and request.session.get("userid") != None:
        try:
            item ={
                "userId": request.session["userid"]
            }
            _result = await dbConnect.queryMeMemb(item)
            if _result != None:
                content = {
                    "data": _result
                }
                return JSONResponse(content)
        except Exception:
            print("連線錯誤。")

    return JSONResponse({"error": True})
