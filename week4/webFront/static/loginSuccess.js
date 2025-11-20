const logoutBtn = document.getElementById('logout-Btn');
logoutBtn.addEventListener('click', logout);

document.addEventListener('DOMContentLoaded', async function() {
    const hotel_Json = window.APP_JSON;
    // 取得key值
    const keyArr = Object.keys(hotel_Json);
    // 取得key有幾個
    const keyLength = Object.keys(hotel_Json).length;
    //console.log(keyArr[1]);
    //console.log(keyArr[0]);
    const title = document.getElementById('title-Str');
    const msg = document.getElementById('message-Str');

    if (keyArr[1] == "result" && keyArr[0] == "func" && keyLength == 2) {
        if (hotel_Json.func == "search"){
            const hotelInfo = hotel_Json.result;
            
            title.textContent = "旅館的資訊";
            msg.textContent = hotelInfo;
            logoutBtn.textContent = "返回首頁";

        }
        else if (hotel_Json.func == "login"){
            title.textContent = "歡迎光臨，這是會員頁";
            msg.textContent = "恭喜您，成功登入系統";
            logoutBtn.textContent = "登出系統";
        }
        
    }
    
});


// 成功的頁面
async function logout(){
    if (logoutBtn.textContent == "登出系統"){
        try{
            const response = await fetch('/logout',{method: 'GET'});
            const result = await response.json();

            if (!response.ok){
                    throw new Error("HTTP Error, status:", response.status);
            }else{
                    window.location.href= result.page;
            }

        }catch (error) {
            console.log('串接錯誤:', error);
        }
    }else if(logoutBtn.textContent == "返回首頁"){
        try{
                window.location.href = "/";
        }catch{
            console.log('串接錯誤:', error);
        }
    }
    
}


