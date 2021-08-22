from aiogram import md, types

from aiogram_bot.misc import dp, i18n
from aiogram_bot.services.hastebin import hastebin

_ = i18n.gettext


@dp.message_handler(commands=["paste"])
async def command_paste(message: types.Message):
    if message.reply_to_message:
        dst = message.reply_to_message
        content = message.reply_to_message.text
    else:
        dst = message
        content = message.get_args()
    if not content:
        return

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
    await dst.reply(text)
