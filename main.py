import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
import asyncio

bot = Bot(token="YOUR_TOKEN", parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Языки и выбор
LANGS = {
    "🇺🇿 O‘zbek": "uz",
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en"
}
user_langs = {}

def language_keyboard():
    buttons = [[KeyboardButton(lang)] for lang in LANGS.keys()]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Загрузка данных
with open("places.json", "r", encoding="utf-8") as f:
    places = json.load(f)

def city_keyboard(lang="ru"):
    unique_cities = []
    for place in places:
        name = place["city"].get(lang, place["city"]["ru"])
        if name not in unique_cities:
            unique_cities.append(name)
    buttons = [[KeyboardButton(city)] for city in unique_cities]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text.in_(LANGS.keys()))
async def set_language(message: Message):
    lang_code = LANGS[message.text]
    user_langs[message.from_user.id] = lang_code
    await message.answer("✅ Язык выбран.\n\nВыберите город:", reply_markup=city_keyboard(lang_code))

@dp.message(F.text.lower().in_(["start", "начать", "/start"]))
async def start(message: Message):
    await message.answer("Выберите язык / Choose language / Tilni tanlang:", reply_markup=language_keyboard())

@dp.message()
async def handle_city(message: Message):
    user_id = message.from_user.id
    lang = user_langs.get(user_id, "ru")
    city_query = message.text.strip()

    response = ""
    for place in places:
        city_name = place["city"].get(lang, place["city"]["ru"])
        if city_query.lower() == city_name.lower():
            if not response:
                response += f"🏙️ {city_name}:\n\n"
            response += f"📍 <b>{place['name'][lang]}</b>\n"
            response += f"{place['description'][lang]}\n"
            response += f"📌 {place['address'][lang]}\n"
            response += f"🧭 {place['directions'][lang]}\n\n"

    if response:
        await message.answer(response, parse_mode="HTML")
    else:
        await message.answer("Пожалуйста, выберите город из меню.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
