from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart
from aiogram.utils.markdown import hbold, hlink, quote_html
from app.misc import dp, i18n
from app.models.chat import Chat
from app.models.user import User
from loguru import logger

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
        _("{command} - Start conversation with bot").format(command="/start"),
        _("{command} - Get this message").format(command="/help"),
        _("{command} - Chat or user settings").format(command="/settings"),
        "",
    ]

    if types.ChatType.is_private(message):
        text.extend(
            [
                # hbold(_("Available only in PM with bot:")),
                # "",
                _("In chats this commands list can be other")
            ]
        )
    else:
        text.extend(
            [
                hbold(_("Available only in groups:")),
                _("{command} - Report message to chat administrators").format(
                    command="/report, !report, @admin"
                ),
                _("{command} - Set RO mode for user").format(command="!ro"),
                _("{command} - Ban user").format(command="!ban"),
                "",
                _("In private chats this commands list can be other"),
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
