import logging
import os
import json
import gspread
from aiogram import Bot, Dispatcher, executor, types
from oauth2client.service_account import ServiceAccountCredentials

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS = json.loads(os.getenv("GOOGLE_CREDENTIALS", "{}"))

# Настройка Telegram бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я бот для учёта запчастей и заказов.")

@dp.message_handler(commands=["stock"])
async def stock_cmd(message: types.Message):
    try:
        data = sheet.get_all_records()
        if not data:
            await message.answer("Список запчастей пуст.")
            return
        text = "\n".join([f"{row['Название']}: {row['Остаток']}" for row in data])
        await message.answer(f"📦 Остатки запчастей:\n{text}")
    except Exception as e:
        await message.answer(f"Ошибка при получении данных: {e}")

@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    await message.answer(
        "/start — Приветствие\n"
        "/stock — Посмотреть остатки запчастей\n"
        "/help — Помощь"
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)