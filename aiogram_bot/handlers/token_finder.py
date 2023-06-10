from aiogram import Bot, types
from aiogram.dispatcher.handler import SkipHandler

from aiogram_bot.misc import dp, i18n

_ = i18n.gettext


@dp.message_handler(
    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP], contains_bot_token=True
)
async def found_token_in_msg(message: types.Message, token: str):
    try:
        temp_bot = Bot(token, validate_token=True)
        temp_bot_data = await temp_bot.get_me()
    except Exception:
        raise SkipHandler
    else:
        await message.reply(
            _(
                "[ALERT] You posted a token, go revoke it with @BotFather.\n\nToken exposed: @{exposed_bot_username}"
            ).format(exposed_bot_username=temp_bot_data.username)
        )
