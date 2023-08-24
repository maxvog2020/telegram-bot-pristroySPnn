let tg = window.Telegram.WebApp;

tg.expand();

let main_button = tg.MainButton;
main_button.text = "Главная кнопка";
main_button.show();

let back_button = tg.BackButton;
back_button.show();

document.getElementById("test").remove();
console.log("Test");
