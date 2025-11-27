const _formSignUp = document.getElementById('signUp-form');
document.addEventListener('DOMContentLoaded', function(){
    if (_formSignUp){
    _formSignUp.addEventListener('submit', function(event){
        event.preventDefault();
    });
}
})

const _formLoggin = document.getElementById('login-form');
document.addEventListener('DOMContentLoaded', function(){
    if (_formLoggin){
    _formLoggin.addEventListener('submit', function(event){
        event.preventDefault();
    });
    }
})

const SUBtn = document.getElementById('sign-info');
if (SUBtn){
    SUBtn.addEventListener('click', signUpMember);
}

async function signUpMember(){
    const userInfo = {
        name: _formSignUp[0].value,
        email: _formSignUp[1].value,
        pw: _formSignUp[2].value
    };
    console.log("執行註冊功能");
    if (userInfo.name !== '' && userInfo.email !== '' && userInfo.pw != ''){
        try{
            const response = await fetch('/signup', {method: 'POST',
                            headers:{
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(userInfo),
                            })

            if (!response.ok){
                throw new Error("HTTP Error, Status:", response.status);
            }else{
                console.log('註冊成功');
                window.location.href=response.url;
            }
        }catch(error){
            console.log("註冊過程中發生錯誤。");
        }
    }
}

const logBtn = document.getElementById('login-info');
if (logBtn){
    logBtn.addEventListener('click', loginWeb);
}

async function loginWeb() {
    const logInfo = {
        email: _formLoggin[0].value,
        password: _formLoggin[1].value
    };

    if(logInfo.email !== '' && logInfo.password !== ''){
        try{
            const response = await fetch('/login', {method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                                },
                            body: JSON.stringify(logInfo)
                            })//.then(data => {
                            //     const url = data["url"];
                            //     const userName = {name: data["name"]};
                            //     // 將資料放至sessionStorage.setItem，以便之後跳頁還是可以取得資料
                            //     sessionStorage.setItem("name", JSON.stringify(userName));
                            //     window.location.href = url;
                            // }).catch(error => {
                            //     throw new Error('HTTP ERROR, Status:', response.status);
                            // });                        
            if(!response.ok){
                throw new Error('HTTP ERROR, Status:', response.status);
            }else{
                window.location.href = response.url;
            }
        }catch(error){
            console.log('登入在檢查資料時，發生錯誤。');
        }
    }
}