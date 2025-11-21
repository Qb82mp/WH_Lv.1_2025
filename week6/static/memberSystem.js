const _formOne = document.getElementById('form_one');
if (_formOne){
    // 若button的type為submit，但不要透過submit跳轉，可以使用下列方式，
    // 將阻止submit跳轉預設的行為。
    _formOne.addEventListener('submit', function(event) {
        event.preventDefault();
    });
}

const registerSubmit = document.getElementById('register_btn');
register_btn.addEventListener('click', registerMember);

async function registerMember() {
    // const nameInfo = document.getElementById('name_text');
    // const emailInfo = document.getElementById('email_text');
    // const passInfo = document.getElementById('pw_text');

    const userDataToSend = {
        name: _formOne[0].value,
        email: _formOne[1].value,
        password: _formOne[2].value
    }

    if (userDataToSend.name !== '' && userDataToSend.email !== '' && userDataToSend.password !== ''){
        try{
            const response = await fetch("/signup", {method: "POST",
                            headers: {
                                    'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(userDataToSend),
                            });
            if (!response.ok){
                throw new Error("HTTP Error, Status:", response.status);
            }else{
                console.log("完成註冊");
                window.location.href=response.url;
            }
        }catch(error){
            console.log("註冊過程中，發生錯誤:", error);
        }
    }
}

const _formTwo = document.getElementById("form_two");
if (_formTwo){
    _formTwo.addEventListener('submit', function(event){
        event.preventDefault();
    });
}

const loginSubmit = document.getElementById("login_btn");
loginSubmit.addEventListener('click', login);

async function login() {
    const userInfo = new URLSearchParams()
    userInfo.append('userEmail', _formTwo[0].value);
    userInfo.append('pw', _formTwo[1].value);

    if (_formTwo[0].value !== "" && _formTwo[1].value !== ""){
        try{
            const response = await fetch('/login', {method: "POST",
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            body: userInfo
            });

            window.location.href = response.url;
        }catch(error){
            console.log("登入過程中，發生錯誤:", error);
        }
    } 
}
