document.addEventListener('DOMContentLoaded', function() {
    // 取得網址的查詢字串，也就是?後面的部分
    const urlPara = new URLSearchParams(window.location.search);

    // 根據參數名稱取該值
    const message = urlPara.get('msg');

    const msgTag = document.getElementById('errorMsg');

    if (msgTag){
        if (message == '信箱或密碼輸入錯誤'){
            msgTag.textContent = "信箱或密碼輸入錯誤 "
        }else if (message == '請輸入信箱和密碼'){
            msgTag.textContent = "請輸入信箱和密碼"
        }
    }else{
        console.log("找不到標籤");
    }
});

