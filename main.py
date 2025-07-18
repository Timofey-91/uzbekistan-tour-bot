import os
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Messege, ReplyKeyboardMarkup, KeybordButton
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Загрузка базы достопримечательностей
with open("places.json", "r", encoding="utf-8") as f:
  places = json.load(f)

# Получить список всех городов
cities = sprted(set(place["city"] for place in places))

# Клавиатура с выбором города
def city_keyboard():
  buttons = [[KeyboardButton(city)] for city in cities]
  return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text.in_(cities))
async def handle_city(message: Message):
    city = message.text
    response = f"🏙️ Достопримечательности {city}:\n\n"
    for place in places:
        if place["city"] == city:
            response += f"📍 <b>{place['name']}</b>\n"
            response += f"{place['description']}\n"
            response += f"📌 Адрес: {place['address']}\n"
            response += f"🧭 Как добраться: {place['directions']}\n\n"
    await message.answer(response, parse_mode="HTML")

@dp.message()
async def start(message: Message):
    await message.answer(
        "Привет! Я бот-гид по городам Узбекистана 🇺🇿\n\nВыбери город, чтобы узнать о его достопримечательностях:",
        reply_markup=city_keyboard()
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
