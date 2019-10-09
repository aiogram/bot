from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(LoggingMiddleware("bot"))
