import asyncio
import logging
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Загрузка переменных окружения
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена в .env файле")

# Создание диспетчера
dp = Dispatcher()

# Кнопки для выбора языка
language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
    [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")]
])

# Хендлер команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer("🌐 Выберите язык / Tilni tanlang:", reply_markup=language_keyboard)

# Хендлер нажатий на кнопки выбора языка
@dp.callback_query(F.data.startswith("lang_"))
async def language_selected(callback: CallbackQuery):
    lang = callback.data.split("_")[1]

    if lang == "ru":
        text = f"👋 Привет, {html.bold(callback.from_user.full_name)}! Добро пожаловать!"
    elif lang == "uz":
        text = f"👋 Salom, {html.bold(callback.from_user.full_name)}! Xush kelibsiz!"
    else:
        text = "Язык не поддерживается / Til qo'llab-quvvatlanmaydi."

    await callback.message.edit_text(text)  # Изменяет предыдущее сообщение с кнопками
    await callback.answer()  # Убирает "часики" на кнопке

# Обработчик любых сообщений — echo
@dp.message()
async def echo_handler(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Не могу отправить это сообщение 😅")

# Основной запуск
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())