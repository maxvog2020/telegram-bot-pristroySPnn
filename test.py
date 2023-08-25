from config import config
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy
import json


TOKEN = config.bot_token.get_secret_value()
CHAT_ID = config.chat_id.get_secret_value()
MODER = config.moder.get_secret_value()
WEB_PREFIX = "https://maxvog2020.github.io/telegram-bot-test/web"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

#########################
async def test_callback(message: Message, values):
    print(message.text)

callbacks = {
    "test_callback": test_callback,
}

#########################
async def publish(message: Message, values):
    callback = values.get('callback')
    await callback(message, values)

@dp.message(F.photo)
async def on_get_photo(message: Message, state: FSMContext):
    values = await state.get_data()
    image_count = values.get('image_count') or 0
    images = values.get('images') or []

    if image_count == 0:
        await message.delete()
        return
    else:
        images.append(message)
        image_count -= 1
        await state.update_data(images=images, image_count=image_count)

    if image_count == 0:
        publish(message, values)


@dp.message(F.web_app_data)
async def on_get_data(message: Message, state: FSMContext):
    data = message.web_app_data.data
    user = message.from_user

    await message.delete()
    
    json_data = json.loads(data)
    callback = callbacks[json_data['callback']]
    image_count = json_data['image_count']

    await state.update_data(callback=callback, image_count=image_count, json_data=json_data)
    if image_count == 0:
        publish(message, await state.get_data())


@dp.callback_query()
async def on_callbacks(callback: CallbackQuery, state: FSMContext):
    url = WEB_PREFIX + callback.data

    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text="Перейти в меню", web_app=WebAppInfo(url=url)))

    message = await callback.message.answer(text="Нажмите на кнопку для перехода в меню", reply_markup=markup.as_markup())

    await callback.answer()
    await asyncio.sleep(3)
    await message.delete()

@dp.message(Command("start"))
async def on_start(message: Message):
    markup = InlineKeyboardBuilder()

    markup.add(InlineKeyboardButton(text="Создать объявление", callback_data="/"))

    await message.answer("<b>➡️ Меню ⬅️</b>", reply_markup=markup.as_markup(), parse_mode="HTML")
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
