// Task4
function getURLContent() {
    attractionConten("https://cwpeng.github.io/test/assignment-3-1").then(textData => {

        attractionConten("https://cwpeng.github.io/test/assignment-3-2").then(imgData => {
            //console.log(Data);
            dataProcess(textData, imgData);
        })

    })
}

const attractionConten = async (webURL) => {
    let webContent = null;
    try{
        const response = await fetch(webURL, {
            method: 'GET',
            mode: 'cors',
            credentials: 'same-origin',
            // headers: {
            //     'Content-Type': 'application/json',
            //     'X-CSRF-Token': 'YOUR_CSRF_TOKEN',
            //     'Access-Control-Allow-Origin': 'GET, POST, PUT, DELETE, OPTIONS'
            // }
        })

        if (!response.ok){
            throw new Error('HTTP Error, status:', response.status);
        }

        // 使用await等待，response物件轉為JSON格式
        webContent = await response.json();

        return webContent;
    } catch (error){
        console.log('Error:',{error});
        throw error;
    }
}

const contentList = {}
async function dataProcess(textData, imgData){
    //url_host = Data.host; 
    //console.log();
    // 將json格是一個一個資料做處理
    //用成{'2012021000000001': ['華中河濱公園', '圖片位置'], 
    //     '2011051800000125': ['自來水博物館', '圖片位置']}
    for (let i =0;i < textData['rows'].length; i++){
        let textDict = textData['rows'][i];
        let key = textDict["serial"];
        contentList[key] = [textDict["sname"]];
    }

    //console.log(contentList);
    url_host = imgData.host;
    for (let j=0; j < imgData['rows'].length; j++){
        let imgDict = imgData['rows'][j]
        let imgPath, imgPathSplit, imgPathFirst, imgHref;

        if (imgDict['serial'] in contentList){
            imgPath = imgDict['pics'];
            imgPathSplit = imgPath.split(".jpg");
            imgPathFirst = imgPathSplit[0] + ".jpg";
            imgHref = url_host + imgPathFirst;

            let key = imgDict['serial'];
            contentList[key].push(imgHref);
        }
    }

    console.log(contentList);
    originalUI();
}


function originalUI(){
    const firstPartParent = document.getElementById('firstPart');
    const secondPartParent = document.getElementById('secondPart');
 
    let i = 1;
    let j = 1;
    for(key in contentList){
        if (i <= 3 && firstPartParent){
                // 新增外框架
                const newTag = document.createElement('div');
                // 設定外框架的類別
                let newTagClassName = 'bar' + String(i);
                newTag.classList.add(newTagClassName);

                // 新增框架內的圖片與內容顯示的部分
                const imgTag = document.createElement('img');
                const titleTag = document.createElement('span');
                // 設定內部的資料
                imgTag.src = contentList[key][1];
                titleTag.textContent = contentList[key][0];
                newTag.appendChild(imgTag);
                newTag.appendChild(titleTag);

                firstPartParent.appendChild(newTag);
        }

        if (i > 3 && secondPartParent){
            console.log(secondPartParent);
            // 新增外框架
            const newTag = document.createElement('div');
            // 設定外框架的類別
            let newTagClassName = 'b' + String(j);
            newTag.classList.add("sec_block",newTagClassName);
            secondPartParent.appendChild(newTag);

            // 新增框架內的圖片與內容顯示的部分
            const img1Tag = document.createElement('img');
            const img2Tag = document.createElement('img');
            const titleContainer = document.createElement('span');
            const titleText = document.createElement('div');

            // 設定內部的資料
            img1Tag.classList.add("bgImg");
            img1Tag.src = contentList[key][1];

            img2Tag.classList.add("star");
            img2Tag.src = "star.png";

            titleContainer.classList.add("sec_text");

            titleText.classList.add('text-content');
            titleText.textContent = contentList[key][0];
            titleContainer.appendChild(titleText);


            newTag.appendChild(img1Tag);
            newTag.appendChild(titleContainer);
            newTag.appendChild(img2Tag);

            j++;
        }
        
        if (i == 13){
            //taipeiData = contentList;
            break;
        }

        i++;
    }
}

// 監聽載入按鈕的動作
const loadButton = document.getElementById('loadBtn');

let dataListIdx = 13;  // 計算當下撈取資料停止的位置，等待下一次新增元素的執行
let sec_block_number = 11; // 紀錄第三區塊中10個bloc的block部分，有幾個block數量
let taipeiData = structuredClone(contentList); // 深拷貝資料
function loadFunc(){
    console.log("點擊");
    const secondPartParent = document.getElementById('secondPart');
    //const currentRows = secondPartParent.style.gridTemplateRows;
    let addElement = 0; // 計算已經撈取10個資料了
    const listLength = Object.keys(contentList).length;
    let loopCount = 1; // 計算取回圈數量

    for(key in contentList){        
        if (loopCount > dataListIdx){
            console.log(String(listLength));

            if (addElement >= 10 || listLength == loopCount){
                if (listLength == loopCount){
                    //secondPartParent.style.gridTemplateRows = currentRows + " 227px";
                    loadButton.style.display = "none";
                }
                // else{
                //     secondPartParent.style.gridTemplateRows = currentRows + " 227px 227px";
                // }
                
                break;
            }

            // 新增外框架
            const newTag = document.createElement('div');
            // 設定外框架的類別
            let newTagClassName = 'b' + String(sec_block_number);
            newTag.classList.add("sec_block",newTagClassName);
            secondPartParent.appendChild(newTag);

            // 新增框架內的圖片與內容顯示的部分
            const img1Tag = document.createElement('img');
            const img2Tag = document.createElement('img');
            const titleContainer = document.createElement('span');
            const titleText = document.createElement('div');

            // 設定內部的資料
            img1Tag.classList.add("bgImg");
            img1Tag.src = contentList[key][1];

            img2Tag.classList.add("star");
            img2Tag.src = "star.png";

            titleContainer.classList.add("sec_text");

            titleText.classList.add('text-content');
            titleText.textContent = contentList[key][0];
            titleContainer.appendChild(titleText);


            newTag.appendChild(img1Tag);
            newTag.appendChild(titleContainer);
            newTag.appendChild(img2Tag);

            dataListIdx++;
            addElement++;
            

            sec_block_number++; // 紀錄second block的編號
        }

        loopCount++;
    }

}

// 將該件是設定監聽觸發的事件
// element.addEventListener(事件類型, 執行的函數)
loadButton.addEventListener('click', loadFunc);


getURLContent();

