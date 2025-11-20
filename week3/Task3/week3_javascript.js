// Task3
function getURLContent() {
    // 取得文字內容
    //const textContent = attractionConten("https://cwpeng.github.io/test/assignment-3-1");
    // 取得圖片位置
    //const List = null;
    attractionConten("https://cwpeng.github.io/test/assignment-3-1").then(textData => {

        attractionConten("https://cwpeng.github.io/test/assignment-3-2").then(imgData => {
            //console.log(Data);
            dataProcess(textData, imgData);
        })

    })
}

async function dataProcess(textData, imgData){
    //url_host = Data.host;
    const contentList = {}
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

    //console.log(contentList);
    funcTask3(contentList);
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

function funcTask3(contentList){
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
            break;
        }

        i++;
    }
}


getURLContent();

