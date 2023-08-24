from config import config
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


TOKEN = config.bot_token.get_secret_value()
CHAT_ID = config.chat_id.get_secret_value()
MODER = config.moder.get_secret_value()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def on_start(message: Message):
    await message.answer("Hello, world!")

#########################
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
