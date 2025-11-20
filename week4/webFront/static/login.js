const loginBtn = document.getElementById('submitBtn');  // 監聽按鈕
loginBtn.addEventListener('click', submit); // 觸發事件

// 會員登入使用
async function submit(){
    // 取得checkbox的 .checked屬性
    const checkProperty = document.getElementById('agreeChecked');

    const _id = document.getElementById('inputId');
    const _pass = document.getElementById('inputPassword');

    //console.log("點擊");
    if (checkProperty.checked == false) {
        alert('請勾選同意條款');
    }else{
        
        const userVerifty = new URLSearchParams();
        userVerifty.append('username', _id.value);
        userVerifty.append('password', _pass.value);

        try{
           const response = await fetch('/login', {method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: userVerifty
            });

            const verifyResult = await response.json();
            if (verifyResult.status == 200)
            {
                window.location.href = `/member`;
            }else{
                const para = {"msg": verifyResult.username};
                // 將物件轉為"msg=自訂資訊"的格式
                const urlParaPath =  new URLSearchParams(para);
                window.location.href = `/ohoh?${urlParaPath.toString()}`;
            }

        }catch (error) {
            console.log('串接錯誤:', error);
        }
    }
}


// 負責處理旅館資訊的查詢頁面
const hotelBtn = document.getElementById('searchBtn');
hotelBtn.addEventListener('click', search);

async function search() {
    const _searchNumber = document.getElementById('inputNumber');
    const inputText = _searchNumber.value;


    // 使用正規表達式檢查輸入的值，是否為純整數
    let is_number = /^\d+$/.test(inputText); 
    if (is_number == true){
        const hotel_ID = parseInt(inputText);
        try{
            // 網址變數的部分，要使用反引號 (`)
            window.location.href= `/hotel/${hotel_ID}`;
               
        }catch (error){
            console.log('串接錯誤:', error);
        }      
    }else{
        alert("請輸入正整數");
    }
}