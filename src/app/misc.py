from aiogram import Bot, Dispatcher, types

from app import config

bot = Bot(config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
