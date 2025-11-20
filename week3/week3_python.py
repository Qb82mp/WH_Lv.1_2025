# Task1
import urllib.request
import json
import re
import html

def func1():
    # 撈取url的資料
    # 設定要撈取的網址
    urlCh = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
    urlEn = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
    chStr = ""
    enStr = ""

    try:
        with urllib.request.urlopen(urlCh) as contentCh:
            # 讀取網頁的回應的內容
            chStr = contentCh.read().decode('utf-8-sig')
    except urllib.error.HTTPError as e:
        print(f"中文資料網頁發生HTTP錯誤:狀態碼為{e.code}")
    except urllib.error.URLError as e:
        print(f"中文資料網頁發生URL的連線錯誤:{e.reason}")
    except Exception as e:
        print(f"中文資料網頁其他錯誤:{e}")

    try:
        with urllib.request.urlopen(urlEn) as contentEn:
            # 讀取網頁的回應的內容
            enStr = contentEn.read().decode('utf-8-sig')
    except urllib.error.HTTPError as e:
        print(f"英文資料網頁發生HTTP錯誤:狀態碼為{e.code}")
    except urllib.error.URLError as e:
        print(f"英文資料網頁發生URL的連線錯誤:{e.reason}")
    except Exception as e:
        print(f"英文資料網頁其他錯誤:{e}")

    if chStr != "" and enStr != "":
        # 將網頁內容轉換成python看得懂的json格式
        jsonCh = json.loads(chStr)
        jsonEn = json.loads(enStr)
        
        hotelList = {}
        districtList = {}
        for itemCh in jsonCh['list']:
            _idCh = itemCh['_id']
            chName = itemCh['旅宿名稱']
            chAddressAll = itemCh['地址']
            Address_split = chAddressAll.split('區')
            chAddressRoad = Address_split[1]
            hotelList[_idCh] = [_idCh, chName, chAddressRoad]

            # 取得行政區
            address_split_city = chAddressAll.split("市")
            address_split_district = address_split_city[1].split("區")
            addressDist = address_split_district[0] + "區"
            hotelCount = 0
            roomCount = 0
            if addressDist in districtList:
                hotelCount = districtList[addressDist][0] + 1
                roomCount = districtList[addressDist][1] + int(itemCh["房間數"])

                districtList[addressDist][0] = hotelCount
                districtList[addressDist][1] = roomCount

            else:
                districtList[addressDist] = [1, int(itemCh["房間數"])]
        
        for key in districtList:    
            with open('districts.csv', 'a', encoding='utf-8') as distF:
                distContent = key + "," + str(districtList[key][0]) + "," + str(districtList[key][1]) + "\n"
                distF.write(distContent)


        for itemEn in jsonEn['list']:
            _idEn = itemEn['_id']
            enName = itemEn['hotel name']
            enAddressAll = itemEn['address']
            # 判斷HTML/XML的編碼
            if "&#" in enAddressAll:
                enAddressAll = html.unescape(enAddressAll)
            enTel = itemEn['tel']
            roomNum = itemEn['the total number of rooms']

             # 處理地址顯示的範圍
            enAddress = ""
            # 使用split分割時，用flags=re.IGNORECASE可以忽略字母大小寫
            enAddressAll_split_city = re.split("Taipei", enAddressAll, flags=re.IGNORECASE)
            if "Rd" in enAddressAll_split_city[0] or " rd" in enAddressAll_split_city[0]:
                item_split = re.split("Rd", enAddressAll_split_city[0], flags=re.IGNORECASE)
                enAddress = item_split[0] + "Rd.,"
            elif "St" in enAddressAll_split_city[0] and enAddress == "":
                item_split = enAddressAll_split_city[0].split("St")
                enAddress = item_split[0] + "St.,"
            elif "Road" in enAddressAll_split_city[0] and enAddress == "":
                item_split = enAddressAll_split_city[0].split("Road")
                enAddress = item_split[0] + "Road."
            elif enAddress == "":
                item_split = enAddressAll_split_city[0].split(",")
                for item in item_split:
                    if "Dist" in item or "DIST" in item:
                        continue
                    if " " == item:
                        continue
                    enAddress += item + ","


            with open('hotels.csv', 'a', encoding='utf-8') as f:
                content_line = ""
                if enAddress[-1] != ",":
                    content_line = hotelList[_idEn][1] + ","+ enName + "," + hotelList[_idEn][2] + "," + enAddress + "," + enTel + "," + roomNum + "\n"
                else:
                    content_line = hotelList[_idEn][1] + ","+ enName + "," + hotelList[_idEn][2] + "," + enAddress + enTel + "," + roomNum + "\n"
                f.write(content_line)
      
func1()




# Task2
from bs4 import BeautifulSoup
from datetime import datetime
class BS4Web:
    def func2(self):
        titleDiv = ""
        pageList = self.findURLOfThreePages()
        for html in pageList:
            if isinstance(html, BeautifulSoup):
                titleDiv = html.find_all('div', class_="title")
            else:
                with urllib.request.urlopen(html) as contentCh:
                    # 讀取網頁的回應的內容
                    getContent = contentCh.read().decode('utf-8-sig')
            
                # 使用html.parser解析器解析網頁架構
                htmlDOM = BeautifulSoup(getContent, "html.parser")
                # 找html架構中所有標籤為div，且class設定等於title，轉為list呈現
                titleDiv = htmlDOM.find_all('div', class_="title")


            for item in titleDiv:
                titleAhref = item.get_text(strip=True)  # 取得標籤中的內容(文字)
                if "本文已被刪除" not in titleAhref:
                    # 進到文章的網頁進行取得時間與like數量
                    if isinstance(item, int):
                        continue
                    urlArticle = "https://www.ptt.cc/" + item.find('a')['href']
                    with urllib.request.urlopen(urlArticle) as content:
                        # 讀取網頁的回應的內容
                        articleContent = content.read().decode('utf-8-sig')
                    # 使用html.parser解析器解析網頁架構
                    articleHtmlDOM = BeautifulSoup(articleContent, "html.parser")
                    pushTag = articleHtmlDOM.find_all('span', class_="hl push-tag")
                    timeTag = articleHtmlDOM.find_all('span', class_="article-meta-value")
                    if timeTag == []:
                        timeTag = articleHtmlDOM.find_all('span', class_="b4")
                        
                    timeStr = timeTag[-1].get_text()
                    if timeStr[0] == " ":
                        timeStr= timeStr[1:]
                        
                    # print(str(len(pushTag)))
                    # print(timeStr)
                    # print(titleAhref)
                    timeFormat = self.timeFormatIsTrueOrNot(timeStr)
                
                    if timeFormat:
                        with open('articles.csv', 'a', encoding='utf-8') as f:
                            content = titleAhref + "," + str(len(pushTag)) + "," + timeStr + "\n"
                            f.write(content)


    def findURLOfThreePages(self):
        urlArticleTotal= "https://www.ptt.cc/bbs/Steam/index.html"
        with urllib.request.urlopen(urlArticleTotal) as contentCh:
                # 讀取網頁的回應的內容
                getContent = contentCh.read().decode('utf-8-sig')
        
        # 使用html.parser解析器解析網頁架構
        htmlDOM = BeautifulSoup(getContent, "html.parser")

        # 找上一頁網址
        tagPreviousPage = htmlDOM.find_all('a', class_ = "btn wide")
        urlPreviousPage_p1 = "https://www.ptt.cc" + tagPreviousPage[-2]['href']

        p2UrlProcessOne = urlPreviousPage_p1.replace(".html", "")
        p2UrlProcessTwo = p2UrlProcessOne.split("index")
        p2UrlProcessThree = int(p2UrlProcessTwo[-1]) - 1
        urlPreviousPage_p2 = "https://www.ptt.cc/bbs/Steam/index" + str(p2UrlProcessThree) + ".html"
        return [htmlDOM, urlPreviousPage_p1, urlPreviousPage_p2]

    def timeFormatIsTrueOrNot(self, timeStr):
        try:
            datetime.strptime(timeStr, "%a %b %d %H:%M:%S %Y")
            return True
        except ValueError:
            return False

bs4Class = BS4Web()
bs4Class.func2()
