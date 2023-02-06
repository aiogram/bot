from typing import Tuple

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hbold

from aiogram_bot.misc import i18n
from aiogram_bot.models.chat import Chat
from aiogram_bot.models.user import User

cb_chat_settings = CallbackData("chat", "id", "property", "value")
cb_user_settings = CallbackData("user", "property", "value")

_ = i18n.gettext

FLAG_STATUS = ["❌", "✅"]

PROPERTY_JOIN = "join"
PROPERTY_BAN_CHANNELS = "ban_channels"
PROPERTY_DEL_CHANNEL_MESSAGES = "del_channel_messages"
PROPERTY_LANGUAGE = "language"


def get_chat_settings_markup(
    telegram_chat: types.Chat, chat: Chat
) -> Tuple[str, InlineKeyboardMarkup]:
    return (
        _("Settings for chat {chat_title}").format(chat_title=hbold(telegram_chat.title)),
        InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("{status} Join filter").format(
                            status=FLAG_STATUS[chat.join_filter]
                        ),
                        callback_data=cb_chat_settings.new(
                            id=chat.id, property=PROPERTY_JOIN, value="switch"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("{status} Ban channels").format(
                            status=FLAG_STATUS[chat.ban_channels]
                        ),
                        callback_data=cb_chat_settings.new(
                            id=chat.id, property=PROPERTY_BAN_CHANNELS, value="switch"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("{status} Delete channel messages").format(
                            status=FLAG_STATUS[chat.delete_channel_messages]
                        ),
                        callback_data=cb_chat_settings.new(
                            id=chat.id, property=PROPERTY_DEL_CHANNEL_MESSAGES, value="switch"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("{flag} Language").format(
                            flag=i18n.AVAILABLE_LANGUAGES[i18n.ctx_locale.get()].flag
                        ),
                        callback_data=cb_chat_settings.new(
                            id=chat.id, property=PROPERTY_LANGUAGE, value="change"
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


def get_user_settings_markup(chat: Chat, user: User) -> Tuple[str, InlineKeyboardMarkup]:
    return (
        _("Personal settings"),
        InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("{status} Do not disturb").format(
                            status=FLAG_STATUS[user.do_not_disturb]
                        ),
                        callback_data=cb_user_settings.new(
                            property="do_not_disturb", value="switch"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("{flag} Language").format(
                            flag=i18n.AVAILABLE_LANGUAGES[chat.language].flag
                        ),
                        callback_data=cb_user_settings.new(property="language", value="change"),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_("Done"),
                        callback_data=cb_user_settings.new(property="done", value="true"),
                    )
                ],
            ]
        ),
    )
