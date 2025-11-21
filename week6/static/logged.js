const logOutButton = document.getElementById("logOut_btn");
if (logOutButton){
    logOutButton.addEventListener('click', logout);
}

async function logout() {
    try{
        const response = await fetch("/logout", {method: "GET"});
        if (response.ok){
            window.location.href=response.url;
        }
    }catch(error){
        console.log("登出過程中，發生錯誤:", error);
    }
    
}

const _msgForm = document.getElementById("msgForm_two");
if(_msgForm){
    _msgForm.addEventListener('submit', function(event){
        event.preventDefault();
    });
}

const inputMsgBtn = document.getElementById("msgInput_btn");
if (inputMsgBtn){
    inputMsgBtn.addEventListener('click', inputMsg);
}

async function inputMsg() {
    if (_msgForm[0].value !== ""){
        const commnetInfo = {
        comment: _msgForm[0].value
        }

        try{
            const response = await fetch("/createMessage", {method: "POST",
                            headers:{
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(commnetInfo),
                            });
            if (!response.ok){
                throw new Error("HTTP Error, Status:", response.status);
            }else{
                window.location.href = response.url;
            }
        }catch(error){
            console.log("新增留言功能，發生錯誤。");
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // 使用forEach的方式，將同個類別下的button裝觸發的監聽功能
    document.querySelectorAll('.delBtn').forEach(deleteBtn => {
        deleteBtn.addEventListener('click', function(event){
            const comm_id = this.dataset.commentId;

            const commStrId = "comm_str"+ String(comm_id);
            const commStr = document.getElementById(commStrId);

            if (commStr){
                commText = commStr.textContent;
                alertMsg = "請確認是否要將『" + commText + "』，此則留言刪除呢?"
                let anser = confirm(alertMsg); 

                if (anser){
                    console.log("已刪除");
                    deleteComment(comm_id);
                }
            }
        });
    });
});


async function deleteComment(delCommId) {
    const commentId = new URLSearchParams()
    commentId.append("commId", delCommId);

    try{
        const response = await fetch("/deleteMessage", {method: "POST",
                        headers:{
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: commentId,
                        });
        if (!response.ok){
            throw new Error("HTTP Error, Status:", response.status)
        }else{
            window.location.href = response.url;
        }
    }catch(error){
        console.log("刪除留言發生錯誤。");
    }
}