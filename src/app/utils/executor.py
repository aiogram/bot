from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from loguru import logger

from app import config
from app.misc import dp
from app.models import db
from app.services import apscheduller

runner = Executor(dp)


async def on_startup_webhook(dispatcher: Dispatcher):
    logger.info("Configure Web-Hook URL to: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)


runner.on_startup(db.on_startup)
runner.on_startup(on_startup_webhook, webhook=True, polling=False)
runner.on_startup(apscheduller.on_startup)
runner.on_shutdown(apscheduller.on_shutdown)
