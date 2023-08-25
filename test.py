from config import config
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy


TOKEN = config.bot_token.get_secret_value()
CHAT_ID = config.chat_id.get_secret_value()
MODER = config.moder.get_secret_value()
WEB_PREFIX = "https://maxvog2020.github.io/telegram-bot-test/web"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

@dp.message(F.photo)
async def on_get_photo(message: Message):
    print("Aaaa")

@dp.message(F.web_app_data)
async def on_get_data(message: Message):
    user = message.from_user
    await message.answer(message.web_app_data.data)
    await message.delete()

@dp.callback_query()
async def on_callbacks(callback: CallbackQuery):
    url = WEB_PREFIX + callback.data

    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text="Создать объявление", web_app=WebAppInfo(url=url)))

    message = await callback.message.answer(text="Нажмите на кнопку для перехода в меню", reply_markup=markup.as_markup())

    await callback.answer()
    await asyncio.sleep(5)
    await message.delete()

@dp.message(Command("start"))
async def on_start(message: Message):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text="Создать объявление", callback_data="/"))

    await message.answer("Some plain text", reply_markup=markup.as_markup())
    await message.delete()

@dp.message()
async def delete_everything_else(message: Message):
    await message.delete()


#########################
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
