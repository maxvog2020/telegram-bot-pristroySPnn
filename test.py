from config import config
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, WebAppInfo, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder


TOKEN = config.bot_token.get_secret_value()
CHAT_ID = config.chat_id.get_secret_value()
MODER = config.moder.get_secret_value()
WEB = config.web

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def on_start(message: Message):
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text="Создать объявление", web_app=WebAppInfo(url=WEB)))
    await message.answer("Нажмите на кнопку", reply_markup=markup.as_markup())


#########################
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
