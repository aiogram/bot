from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart
from aiogram.utils.markdown import hbold, hlink, quote_html
from loguru import logger

from app.misc import dp, i18n
from app.models.chat import Chat
from app.models.user import User

_ = i18n.gettext


@dp.message_handler(CommandStart(), types.ChatType.is_private)
async def cmd_start(message: types.Message, user: User):
    logger.info("User {user} start conversation with bot", user=message.from_user.id)
    await message.answer(
        _(
            "Hello, {user}.\n"
            "Send /help if you want to read my commands list "
            "and also you can change language by sending /settings command.\n"
            "My source code: {source_url}"
        ).format(
            user=hbold(message.from_user.full_name),
            source_url=hlink("GitHub", "https://github.com/aiogram/bot"),
        )
    )

    await user.update(start_conversation=True).apply()


@dp.message_handler(CommandHelp())
async def cmd_help(message: types.Message):
    text = [
        hbold(_("Here you can read the list of my commands:")),
        _("/start - Start conversation with bot"),
        _("/help - Get this message"),
        _("/settings - Chat or user settings"),
        "",
    ]

    if types.ChatType.is_private(message):
        # text.extend([hbold(_("Available only in PM with bot:"))])
        pass
    else:
        text.extend(
            [
                hbold(_("Available only in groups:")),
                _("/report, !report, @admin - Report message to chat administrators"),
                _("!ro - Set RO mode for user"),
                _("!ban - Ban user"),
            ]
        )
    await message.reply("\n".join(text))


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception("Cause exception {e} in update {update}", e=e, update=update)
    return True
