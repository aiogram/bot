from pathlib import Path

from aiogram import Bot, Dispatcher, types

from app import config
from app.middlewares.i18n import I18nMiddleware

app_dir: Path = Path(__file__).parent.parent
locales_dir = app_dir / "locales"

bot = Bot(config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
i18n = I18nMiddleware("bot", locales_dir, default="en")


def setup():
    from app import filters, middlewares

    middlewares.setup(dp)
    filters.setup(dp)

    # noinspection PyUnresolvedReferences
    import app.modules  # Load all application submodules
