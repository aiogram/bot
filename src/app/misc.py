from aiogram import Bot, Dispatcher, types

from app import config

bot = Bot(config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def setup():
    from app import filters, middlewares

    middlewares.setup(dp)
    filters.setup(dp)
