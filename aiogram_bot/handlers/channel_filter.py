from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import BadRequest
from loguru import logger
from magic_filter import F

from aiogram_bot.handlers.simple_admin import command_ban_sender_chat
from aiogram_bot.misc import dp
from aiogram_bot.models.chat import Chat, ChatAllowedChannels


@dp.message_handler(
    F.ilter(F.sender_chat & (F.sender_chat.id != F.chat.id) & ~F.is_automatic_forward),
    content_types=types.ContentTypes.ANY,
)
async def sender_chat_messages_handler(message: types.Message, chat: Chat):
    logger.info("Handled channel message")
    result = False
    target = message.sender_chat

    allowed_channel = await ChatAllowedChannels.get((message.chat.id, target.id))
    if allowed_channel:
        logger.info("Is allowed {}", allowed_channel)
        return False

    if chat.ban_channels:
        logger.info("Check ban channels")
        result = await command_ban_sender_chat(message=message, target=target)

    if chat.delete_channel_messages:
        logger.info("Check delete message")
        logger.info(
            "Delete message from channel {} in chat {}",
            message.sender_chat.id,
            message.chat.id,
        )
        with suppress(BadRequest):
            await message.delete()
            result = True

    return result
