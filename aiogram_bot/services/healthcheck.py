from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from aiohttp_healthcheck import HealthCheck
from loguru import logger

from aiogram_bot import config

health = HealthCheck()


def setup(executor: Executor):
    executor.on_startup(on_startup, webhook=True, polling=False)


async def on_startup(dispatcher: Dispatcher):
    from aiogram_bot.utils.executor import runner

    logger.info("Setup healthcheck")

    health.add_check(check_redis)
    health.add_check(check_postgres)
    health.add_check(check_webhook)
    runner.web_app.router.add_get("/healthcheck", health)


async def check_redis():
    from aiogram_bot.misc import storage

    try:
        redis = await storage.redis()
        info = await redis.info()
    except Exception as e:
        return False, str(e)
    return True, f"Redis {info['server']['redis_version']}"


async def check_postgres():
    from aiogram_bot.models.db import db

    try:
        version = await db.scalar("select version();")
    except Exception as e:
        return False, str(e)
    return True, version


async def check_webhook():
    from aiogram_bot.misc import bot

    webhook = await bot.get_webhook_info()
    if webhook.url and webhook.url == config.WEBHOOK_URL:
        return True, f"Webhook configured. Pending updates count {webhook.pending_update_count}"
    else:
        logger.error("Configured wrong webhook URL {webhook}", webhook=webhook.url)
        return False, "Configured invalid webhook URL"
