from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from loguru import logger

from app import config
from app.misc import dp
from app.models import db
from app.services import apscheduller, join_list

runner = Executor(dp)


async def on_startup_webhook(dispatcher: Dispatcher):
    logger.info("Configure Web-Hook URL to: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)


def setup():
    logger.info("Configure executor...")
    db.setup(runner)
    join_list.setup(runner)
    apscheduller.setup(runner)
    runner.on_startup(on_startup_webhook, webhook=True, polling=False)
