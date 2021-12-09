import asyncio
from contextlib import suppress
from typing import List

from aiogram import types
from aiogram.utils import exceptions
from aiogram.utils.exceptions import BadRequest, Unauthorized
from aiogram.utils.markdown import hlink, quote_html
from babel.dates import format_timedelta
from loguru import logger
from magic_filter import F

from aiogram_bot.misc import bot, dp, i18n
from aiogram_bot.models.chat import Chat
from aiogram_bot.models.user import User
from aiogram_bot.utils.timedelta import parse_timedelta_from_message

_ = i18n.gettext


@dp.message_handler(
    F.ilter(F.reply_to_message.sender_chat),
    commands=["ro", "ban"],
    commands_prefix="!",
    user_can_restrict_members=True,
    bot_can_restrict_members=True,
)
async def command_ban_sender_chat(message: types.Message):
    target = message.reply_to_message.sender_chat
    try:  # Apply restriction
        await message.chat.ban_sender_chat(sender_chat_id=target.id)
        logger.info(
            "Chat {chat} restricted by {admin}",
            chat=target.id,
            admin=message.from_user.id,
        )
    except exceptions.BadRequest as e:
        logger.error("Failed to restrict chat member: {error!r}", error=e)
        return False
    await message.reply_to_message.answer(
        _(
            "Channel {channel} was permanently banned "
            "and the channel owner will no longer be able to send messages here "
            "on behalf of any of his channels."
        ).format(channel=target.mention)
    )
    return True


@dp.message_handler(
    F.ilter(F.reply_to_message),
    commands=["ro"],
    commands_prefix="!",
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
        _("<b>Read-only</b> activated for user {user}. Duration: {duration}").format(
            user=message.reply_to_message.from_user.get_mention(),
            duration=format_timedelta(
                duration, locale=chat.language, granularity="seconds", format="short"
            ),
        )
    )
    return True


@dp.message_handler(
    F.ilter(F.reply_to_message),
    commands=["ban"],
    commands_prefix="!",
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
        _("User {user} <b>banned</b> for {duration}").format(
            user=message.reply_to_message.from_user.get_mention(),
            duration=format_timedelta(
                duration, locale=chat.language, granularity="seconds", format="short"
            ),
        )
    )
    return True


@dp.message_handler(
    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP], text_contains="@admin", state="*"
)
@dp.message_handler(
    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    commands=["report"],
    commands_prefix="!/",
    state="*",
)
async def text_report_admins(message: types.Message):
    logger.info(
        "User {user} report message {message} in chat {chat} from user {from_user}",
        user=message.from_user.id,
        message=message.message_id,
        chat=message.chat.id,
        from_user=message.reply_to_message.from_user.id,
    )
    if not message.reply_to_message:
        return await message.reply(
            _(
                "Please use this command is only in reply to message what do you want to report "
                "and this message will be reported to chat administrators."
            )
        )

    admins: List[types.ChatMember] = await message.chat.get_administrators()
    text = _("[ALERT] User {user} is reported message in chat {chat}.").format(
        user=message.from_user.get_mention(),
        chat=hlink(
            message.chat.title,
            f"https://t.me/{message.chat.username}/{message.reply_to_message.message_id}",
        )
        if message.chat.username
        else quote_html(repr(message.chat.title)),
    )

    admin_ids = [
        admin.user.id for admin in admins if admin.is_chat_admin() and not admin.user.is_bot
    ]
    if admin_ids:
        for admin in await User.query.where(
            User.id.in_(admin_ids) & (User.do_not_disturb == False)  # NOQA
        ).gino.all():  # NOQA
            with suppress(Unauthorized):
                await bot.send_message(admin.id, text)
                logger.info("Send alert message to admin {admin}", admin=admin.id)
            await asyncio.sleep(0.3)

    await message.reply_to_message.reply(_("This message is reported to chat administrators."))


@dp.message_handler(
    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    commands=["do_not_click", "leave"],
    bot_can_restrict_members=True,
)
async def cmd_leave(message: types.Message):
    try:
        await message.chat.unban(user_id=message.from_user.id)
        msg = await message.answer(
            _("User {user} leave this chat...").format(user=message.from_user.get_mention())
        )
    except BadRequest:
        msg = None

    await asyncio.sleep(10)

    with suppress(BadRequest):
        await message.delete()
        if msg:
            await msg.delete()
