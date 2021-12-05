from contextlib import suppress

from aiogram import md, types
from aiogram.types.chat_member import ChatMemberAdministrator, ChatMemberOwner
from aiogram.utils.exceptions import TelegramAPIError

from aiogram_bot.misc import bot, dp, i18n
from aiogram_bot.services.hastebin import hastebin

_ = i18n.gettext


@dp.message_handler(commands=["paste"])
async def command_paste(message: types.Message):
    messages_to_delete = []
    if message.reply_to_message and message.reply_to_message.from_user.id != bot.id:
        content = message.reply_to_message.text or message.reply_to_message.caption
        dst = message.reply_to_message
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if isinstance(member, ChatMemberOwner) or (
            isinstance(member, ChatMemberAdministrator) and member.can_delete_messages
        ):
            messages_to_delete.append(dst)
    else:
        content = message.get_args()
        dst = message
        messages_to_delete.append(dst)

    if not content or (len(content) < 30 and content.count('\n') < 2):
        return await message.reply(_("Content to move is too short!"))

    content = content.encode()
    response = await hastebin.create_document(content)

    document_url = hastebin.format_url(response["key"])
    text = _(
        "Message originally posted by {author} was moved to {url} service\n"
        "Content size: {size} bytes"
    ).format(
        author=dst.from_user.get_mention(as_html=True),
        url=md.hlink("HasteBin", document_url),
        size=len(content),
    )
    await dst.reply(text, allow_sending_without_reply=True)

    for message_to_delete in messages_to_delete:
        with suppress(TelegramAPIError):
            await message_to_delete.delete()
