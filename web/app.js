let tg = window.Telegram.WebApp;

tg.expand();
tg.enableClosingConfirmation()

let main_button = tg.MainButton;
main_button.text = "Опубликовать";
main_button.show();

