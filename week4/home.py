from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json, urllib.request


app = FastAPI()
app.mount("/static", StaticFiles(directory="webFront/static"), name="static")
templates = Jinja2Templates(directory="webFront")

# 載入.env的檔案
#load_dotenv()
# 取得key
#secretKey = os.getenv('API_SECRET_KEY')

origins = ["http://127.0.0.1:8000"]

app.add_middleware(
        SessionMiddleware, 
        secret_key="jsd_@h871ftyu48lg5fusd52!4dr453",
        max_age=None, # 設定86400包存一天時間
        https_only=True,
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "POST",
        "GET"
    ],
    allow_headers=["Content-Type"],
)


@app.get("/", response_class=HTMLResponse, name="Home_Page")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="webLogin.html")


@app.post("/login")
async def login(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if username == "abc@abc.com" and password == "abc":
        print("驗證通過")
        request.session['username'] = "abc@abc.com"
        request.session['is_logged'] = True
        #successPage_url = request.url_for("Success_Page")
        return {"username": username, "status": 200}
        
    elif username == "" or password == "":
        #errorPage_url = request.url_for("Error_Page")
        return {"username": "請輸入信箱和密碼", "status": 401}
    else:
        #errorPage_url = request.url_for("Error_Page")
        return {"username": "信箱或密碼輸入錯誤", "status": 401}


@app.get("/member", response_class=HTMLResponse)
async def memberWeb(request: Request):
    if request.session.get("username") != None:
        if request.session['username'] != "" and request.session['is_logged'] == True:
            info = {"func": "login", "result": "執行成功"}
            content = {
                "request": request,
                "info": info
            }
            
            return templates.TemplateResponse("loginSuccess.html", content)
        else:
            homePage = request.url_for("Home_Page")
            return RedirectResponse(url=homePage, status_code=status.HTTP_302_FOUND)
    else:
            homePage = request.url_for("Home_Page")
            return RedirectResponse(url=homePage, status_code=status.HTTP_302_FOUND)
    

@app.get("/ohoh", response_class=HTMLResponse)
async def errorWeb(request: Request):
    return templates.TemplateResponse(request= request, name="loginError.html")


@app.get("/logout")
def logout(request: Request):
    request.session.pop('username', None)
    request.session.pop('is_logged', None)
    
    homePage = request.url_for("Home_Page")
    return {"page": str(homePage)}


@app.get("/hotel/{hotel_ID}", response_class=HTMLResponse)
async def search(request: Request, hotel_ID: int):
    hotel_info_list = searchHotelData(hotel_ID)

    if hotel_info_list == []:
        info = {"func": "search", "result": "查詢不到相關資料"}
        content = {
            "request": request,
            "info": info
        }
    else:
        searchResult = hotelInfoStr(hotel_info_list)
        searchResult["func"] = "search"
        content = {
            "request": request,
            "info": searchResult,
        }

    return templates.TemplateResponse("loginSuccess.html", content)
    

def hotelInfoStr(infoData):
    try:
        if len(infoData) == 3:
            searchStr = infoData[0] + "、" + infoData[1] + "、" + str(infoData[2])
            return {"result": searchStr}
        else:
            return {"result": "查詢不到相關資料"}
    except IndexError as e:
        print(f'IndexError: 超出索引值的範圍')
        return {"result": "查詢不到相關資料"}

def searchHotelData(num):
    urlCh = 'https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch'
    urlEn = 'https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en'

    chStr = ""
    enStr = ""
    # 取得中文網站的資料
    try:
        with urllib.request.urlopen(urlCh) as contentCh:
            # 取得網頁的回應內容
            chStr = contentCh.read().decode('utf-8-sig')
    except urllib.error.HTTPError as e:
        print(f"中文資料網頁發生HTTP錯誤:狀態碼為{e.code}")
    except urllib.error.URLError as e:
        print(f'中文資料網頁發生URL的連線錯誤:{e.reason}')
    except Exception as e:
        print(f'中文資料網頁其他錯誤:{e}')

    # 取得英文網站的資料
    try:
        with urllib.request.urlopen(urlEn) as contentEn:
            # 取得網頁的回應內容
            enStr = contentEn.read().decode('utf-8-sig')
    except urllib.error.HTTPError as e:
        print(f'英文資料網頁發生HTTP錯誤:狀態碼為{e.code}')
    except urllib.error.URLError as e:
        print(f'英文資料網頁發生URL的連線錯誤:{e.reason}')
    except Exception as e:
        print(f'英文資料網頁其他錯誤:{e}')
    
    hotelDict = []
    try:
        if chStr != "" and enStr != "":
            # 將網頁內容轉為json格式
            chJson = json.loads(chStr)
            enJson = json.loads(enStr)

            for index, chKey in enumerate(chJson["list"]):
                if chKey.get("_id") == num:
                    nameCh = chJson["list"][index]['旅宿名稱']
                    hotelDict = [nameCh]
                    break

            for idx, enKey in enumerate(enJson['list']):
                if enKey.get("_id") == num:
                    nameEn = enJson['list'][idx]['hotel name']
                    phoneNumberEn = enJson['list'][idx]['tel']
                    hotelDict.append(nameEn)
                    hotelDict.append(phoneNumberEn)
                    break
    except KeyError as e:
        print("無法撈取網頁的資訊")
    
    return hotelDict