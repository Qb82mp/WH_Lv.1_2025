document.addEventListener('DOMContentLoaded', function(){
    // 從網址取得要顯示的參數值
    // window.location.search是取得網址?後的內容
    const urlPara = new URLSearchParams(window.location.search);
    // 取得msg參數的值
    const msgStr = urlPara.get('msg');

    const errInfo = document.getElementsByClassName('errorInfoStr');
    if (errInfo){
        console.log(msgStr);
        if (msgStr === "重複的電子郵件"){
            errInfo[0].textContent = "重複的電子郵件";
        }else if(msgStr === "電子郵件或密碼錯誤"){
            errInfo[0].textContent = "電子郵件或密碼錯誤";
        }else if(msgStr === "連線發生錯誤"){
            errInfo[0].textContent = "連線發生錯誤";
        }

    }
})