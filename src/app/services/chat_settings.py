from typing import Tuple

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hbold

from app.misc import i18n
from app.models.chat import Chat

cb_chat_settings = CallbackData("chat", "id", "property", "value")
_ = i18n.gettext


FLAG_STATUS = ["❌", "✅"]


def get_chat_settings_markup(
    telegram_chat: types.Chat, chat: Chat
) -> Tuple[str, InlineKeyboardMarkup]:
    return (
        _("Settings for chat {chat_title}").format(chat_title=hbold(telegram_chat.title)),
        InlineKeyboardMarkup(
            inline_keyboard=[
                # [
                #     InlineKeyboardButton(
                #         text=_("{status} Join filter").format(
                #             status=FLAG_STATUS[chat.join_filter]
                #         ),
                #         callback_data=cb_chat_settings.new(
                #             id=chat.id, property="join", value="switch"
                #         ),
                #     )
                # ],
                [
                    InlineKeyboardButton(
                        text=_("{flag} Language").format(
                            flag=i18n.AVAILABLE_LANGUAGES[chat.language].flag
                        ),
                        callback_data=cb_chat_settings.new(
                            id=chat.id, property="language", value="change"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("Done"),
                        callback_data=cb_chat_settings.new(
                            id=chat.id, property="done", value="true"
                        ),
                    )
                ],
            ]
        ),
    )
