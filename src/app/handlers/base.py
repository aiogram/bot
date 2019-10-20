from aiogram import md, types
from aiogram.dispatcher.filters import CommandStart
from loguru import logger

from app.misc import dp, i18n
from app.models.user import User

_ = i18n.gettext


@dp.message_handler(CommandStart(), types.ChatType.is_private)
async def cmd_start(message: types.Message, user: User):
    logger.info("User {user} start conversation with bot", user=message.from_user.id)
    await message.answer(
        _("Hello, {user}. My source code: {source_url}").format(
            user=md.quote_html(message.from_user.full_name),
            source_url=md.hlink("GitHub", "https://github.com/aiogram/bot"),
        )
    )

    await user.update(start_conversation=True).apply()


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception("Cause exception {e} in update {update}", e=e, update=update)
    return True
