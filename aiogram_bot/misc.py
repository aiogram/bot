from pathlib import Path

import sentry_sdk
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from aiogram_bot import config
from aiogram_bot.middlewares.i18n import I18nMiddleware

app_dir: Path = Path(__file__).parent.parent
locales_dir = app_dir / "locales"

bot = Bot(config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB_FSM)
dp = Dispatcher(bot, storage=storage)
i18n = I18nMiddleware("bot", locales_dir, default="en")

# if config.SENTRY_URL:
#     logger.info("Setup Sentry SDK")
#     sentry_sdk.init(
#         config.SENTRY_URL,
#         traces_sample_rate=1.0,
#     )


def setup():
    from aiogram_bot import filters, middlewares
    from aiogram_bot.utils import executor

    middlewares.setup(dp)
    filters.setup(dp)
    executor.setup()

    logger.info("Configure handlers...")
    # noinspection PyUnresolvedReferences
    import aiogram_bot.handlers
