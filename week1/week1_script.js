/* 控制漢堡選單的使用功能 */

document.addEventListener('DOMContentLoaded', function() {
    const hambergerBtn = document.getElementById('menu_icon');
    const navbarMenu = document.getElementById('navbarMenu');    
    const menuBg = document.getElementById('menu_bg');
    const closeBtn = document.getElementById('menu_close_btn');
    
    if (hambergerBtn){
        hambergerBtn.onclick = function() {
            if (navbarMenu && closeBtn && menuBg){
                hambergerBtn.classList.toggle('active');
                menuBg.classList.toggle('active');
                navbarMenu.classList.toggle('active');
                closeBtn.classList.toggle('active');
            }
            else{
                alert('請確認網頁所有需要使用的功能都已載入，\n若有問題請再確認網路是否正常可以載入網頁，\n謝謝。');
            }

            console.log("按鈕被點擊");
        };
    }

    if (closeBtn){
        closeBtn.onclick = function() {
            if (navbarMenu.classList.contains('active')){
                navbarMenu.classList.remove('active');
                closeBtn.classList.remove('active');
                menuBg.classList.remove('active');
                hambergerBtn.classList.remove('active');
            }
            console.log("關閉點擊");
        }
    }


});

