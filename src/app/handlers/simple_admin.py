from aiogram import types
from aiogram.utils import exceptions
from babel.dates import format_timedelta
from loguru import logger

from app.misc import dp, i18n
from app.models.chat import Chat
from app.utils.timedelta import parse_timedelta_from_message

_ = i18n.gettext


@dp.message_handler(
    commands=["ro"],
    commands_prefix="!",
    is_reply=True,
    user_can_restrict_members=True,
    bot_can_restrict_members=True,
)
async def cmd_ro(message: types.Message, chat: Chat):
    duration = await parse_timedelta_from_message(message)
    if not duration:
        return

    try:  # Apply restriction
        await message.chat.restrict(
            message.reply_to_message.from_user.id, can_send_messages=False, until_date=duration
        )
        logger.info(
            "User {user} restricted by {admin} for {duration}",
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id,
            duration=duration,
        )
    except exceptions.BadRequest as e:
        logger.error("Failed to restrict chat member: {error!r}", error=e)
        return False

    await message.reply_to_message.answer(
        _("Read-only activated for user {user}. duration: {duration}").format(
            user=message.reply_to_message.from_user.get_mention(),
            duration=format_timedelta(duration, locale=chat.language, granularity="seconds"),
        )
    )
    return True


@dp.message_handler(
    commands=["ban"],
    commands_prefix="!",
    is_reply=True,
    user_can_restrict_members=True,
    bot_can_restrict_members=True,
)
async def cmd_ban(message: types.Message, chat: Chat):
    duration = await parse_timedelta_from_message(message)
    if not duration:
        return

    try:  # Apply restriction
        await message.chat.kick(message.reply_to_message.from_user.id, until_date=duration)
        logger.info(
            "User {user} kicked by {admin} for {duration}",
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id,
            duration=duration,
        )
    except exceptions.BadRequest as e:
        logger.error("Failed to kick chat member: {error!r}", error=e)
        return False

    await message.reply_to_message.answer(
        _("User {user} banned for {duration}.").format(
            user=message.reply_to_message.from_user.get_mention(),
            duration=format_timedelta(duration, locale=chat.language, granularity="seconds"),
        )
    )
    return True
