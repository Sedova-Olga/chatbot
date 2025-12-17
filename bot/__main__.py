# bot/__main__.py
import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command
from aiogram import F

# Загрузка токена
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Переменная BOT_TOKEN не задана в .env")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Middleware: логируем все update
@dp.update.middleware()
async def log_all_updates(handler, event: Update, data):
    logging.info(f"📥 Получен update: {event.model_dump_json(indent=2)}")
    return await handler(event, data)


# /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я echo-бот. Отправь текст или фото — я повторю!")


# Обработка текста
@dp.message(F.text)
async def echo_text(message: Message):
    await message.answer(message.text)


# Обработка фото
@dp.message(F.photo)
async def echo_photo(message: Message):
    photo_file_id = message.photo[-1].file_id
    await message.answer_photo(photo=photo_file_id, caption="Вот ваше фото!")


# Запуск
async def main():
    logging.info("🤖 Aiogram Echo Bot запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
