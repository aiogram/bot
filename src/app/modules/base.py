from aiogram import md, types
from aiogram.dispatcher.filters import CommandStart
from loguru import logger

from app.misc import dp, i18n

_ = i18n.gettext


@dp.message_handler(CommandStart(), types.ChatType.is_private)
async def cmd_start(message: types.Message):
    logger.info("User {user} start conversation with bot", user=message.from_user.id)
    await message.answer(
        _("Hello, {user}. My source code: {source_url}").format(
            user=md.quote_html(message.from_user.full_name),
            source_url=md.hlink("GitHub", "https://github.com/aiogram/bot"),
        )
    )
