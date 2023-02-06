import asyncio
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.executor import Executor
from loguru import logger

from aiogram_bot import config
from aiogram_bot.misc import dp
from aiogram_bot.models import db
from aiogram_bot.models.user import User
from aiogram_bot.services import apscheduller, healthcheck, join_list

runner = Executor(dp)


async def on_startup_webhook(dispatcher: Dispatcher):
    logger.info("Configure Web-Hook URL to: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)


async def on_startup_notify(dispatcher: Dispatcher):
    for user in await User.query.where(User.is_superuser == True).gino.all():  # NOQA
        with suppress(TelegramAPIError):
            await dispatcher.bot.send_message(
                chat_id=user.id, text="Bot started", disable_notification=True
            )
            logger.info("Notified superuser {user} about bot is started.", user=user.id)
        await asyncio.sleep(0.2)


def setup():
    logger.info("Configure executor...")
    db.setup(runner)
    join_list.setup(runner)
    apscheduller.setup(runner)
    healthcheck.setup(runner)
    runner.on_startup(on_startup_webhook, webhook=True, polling=False)
    if config.SUPERUSER_STARTUP_NOTIFIER:
        runner.on_startup(on_startup_notify)
