document.addEventListener('DOMContentLoaded', function(){
    // 更新訊息，添加使用者名稱
    const userNameStr = document.getElementById("view-name");
    const user_info = window.APP_INFO;
    const name = user_info.name;
    userNameStr.textContent= name+"，歡迎登入系統";

    searchMe();
});

const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn){
    logoutBtn.addEventListener('click', logOut);
}

async function logOut(){
    window.location.href='/logout';
}

// const _secondForm = document.getElementById('select-form');
// if (_secondForm){
//     _secondForm.addEventListener('submit');
// }
const selectBtn= document.getElementById('select-memb-name');
if (selectBtn){
    selectBtn.addEventListener('click', selectMemb);
}

async function selectMemb(){
    const selectInput = document.getElementById('memb-number');
    if (selectInput){
        const viewMemb = document.getElementById('view-select-info');
        
        const selectNum = selectInput.value.trim();
        //判斷是否為純整數
        const isNumber = /[0-9]/.test(selectNum);
        if (isNumber === true){
            //console.log("確認為數值");
            try{
                //const response = await fetch(`/api/member/${selectNum}`);
                await fetch(`/api/member/${selectNum}`, {method: 'GET'})
                .then(response => {                 
                    const getJsonData = response.json();
                    return getJsonData
                }).then(jsonData => {
                    const getInfo = jsonData.data;
                    return getInfo
                }).then(data => {
                    console.log(data);
                    if (data != null){
                        const viewStr = data.name + " (" + data.email + ")";
                        viewMemb.textContent = viewStr;
                    }else{
                        viewMemb.textContent = "No Data";
                    }      
                }).catch(function(err){
                    console.log("發生錯誤");
                    throw new Error("HTTP ERROR");
                });
            
            }catch{
                console.log("查詢過程中發生錯誤");
            }
           
        }else{
            viewMemb.textContent = "No Data";
        }
        selectInput.value = "";  
    }
}

const changeBtn = document.getElementById('updt-name');
if (changeBtn){
    changeBtn.addEventListener('click', changeName);
}

async function changeName(){
    const changeInput = document.getElementById('up-my-name');
    if (changeInput){
        const viewResult = document.getElementById('view-updt-info');

        const inputStr = changeInput.value.trim();
        const item = {
            "name": inputStr
        }
        try{
            const response = await fetch('/api/member', {method: "PATCH",
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body:JSON.stringify(item),
                            });
            if(!response.ok){
                viewResult.textContent = "Failed to Update";
                throw new Error("HTTP ERROR");
            }else{
                // 非同步的狀態下，在轉換json格式時，需要使用awiat等待
                const getResult = await response.json();
                const _key = Object.keys(getResult);
                if (_key[0] === "ok"){
                    viewResult.textContent = "Updated";
                    const viewUserName = document.getElementById('view-name');
                    if(viewUserName){
                        viewUserName.textContent = inputStr + "，，歡迎登入系統";
                    }               
                }else{
                    viewResult.textContent = "Failed to Update";
                }
            }

        }catch(err){
            viewResult.textContent= "Failed to Update";
        }
        changeInput.value = "";
    }
}

const updateSearchMeBtn = document.getElementById('select-my-name');
if (updateSearchMeBtn){
    updateSearchMeBtn.addEventListener('click', searchMe);
};

async function searchMe(){
    // 取得誰查詢我的使用者資訊
    const viewSearchMe = document.getElementById('view-who-select-my');
    fetch(`/api/search`, {method: "GET"})
    .then(response => {
        const getJSON = response.json();
        return getJSON
    }).then(jsonData => {
        const searchData = jsonData.data;
        if (viewSearchMe){
            if (viewSearchMe.textContent != ""){
                // 清除被包裹新增的子節點(標籤)
                viewSearchMe.textContent = "";
            }
            data_val = Object.values(searchData);
            const createUL = document.createElement('ul');
            viewSearchMe.appendChild(createUL);
            for (let i=0; i<data_val.length; i++){
                const viewInfo = document.createElement('li');
                viewInfo.textContent = data_val[i];
                createUL.appendChild(viewInfo);
            }
        }
    }).catch(err => {
        console.log("發生錯誤");
    });
}

