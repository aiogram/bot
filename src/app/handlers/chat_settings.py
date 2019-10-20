from contextlib import suppress

from aiogram import types
from aiogram.dispatcher.filters.filters import OrFilter
from aiogram.utils.exceptions import MessageCantBeDeleted
from loguru import logger

from app.misc import bot, dp, i18n
from app.models.chat import Chat
from app.models.user import User
from app.services.chat_settings import cb_chat_settings, get_chat_settings_markup
from app.utils.chat_admin import get_chat_administrator

_ = i18n.gettext


@dp.message_handler(
    types.ChatType.is_group_or_super_group, commands=["settings"], user_can_change_info=True
)
async def cmd_chat_settings(message: types.Message, chat: Chat, user: User):
    logger.info("User {user} wants to configure chat {chat}", user=user.id, chat=chat.id)
    with suppress(MessageCantBeDeleted):
        await message.delete()

    text, markup = get_chat_settings_markup(message.chat, chat)
    await bot.send_message(chat_id=user.id, text=text, reply_markup=markup)


@dp.callback_query_handler(cb_chat_settings.filter(property="language", value="change"))
async def cq_chat_settings_language(query: types.CallbackQuery, callback_data: dict):
    target_chat_id = int(callback_data["id"])
    chat = await Chat.query.where(Chat.id == target_chat_id).gino.first()
    if not chat:
        return await query.answer(_("Invalid chat"), show_alert=True)

    markup = types.InlineKeyboardMarkup()

    for code, language in i18n.AVAILABLE_LANGUAGES.items():
        markup.add(
            types.InlineKeyboardButton(
                language.label,
                callback_data=cb_chat_settings.new(id=chat.id, property="language", value=code),
            )
        )

    await query.answer(_("Choose chat language"))
    await query.message.edit_reply_markup(markup)


@dp.callback_query_handler(
    OrFilter(
        *[
            cb_chat_settings.filter(property="language", value=code)
            for code in i18n.AVAILABLE_LANGUAGES
        ]
    )
)
async def cq_chat_settings_choose_language(query: types.CallbackQuery, callback_data: dict):
    target_chat_id = int(callback_data["id"])
    target_language = callback_data["value"]
    chat = await Chat.query.where(Chat.id == target_chat_id).gino.first()
    if not chat:
        return await query.answer(_("Invalid chat"), show_alert=True)

    member = await get_chat_administrator(chat.id, query.message.from_user.id)
    if not member or not member.is_chat_admin():
        await query.answer(_("You cannot change settings of this chat!"), show_alert=True)
        return await query.message.delete()

    await chat.update(language=target_language).apply()
    await query.answer(
        _("Language changed to {new_language}").format(
            new_language=i18n.AVAILABLE_LANGUAGES[target_language].title
        )
    )
    text, markup = get_chat_settings_markup(query.message.chat, chat)
    await query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(cb_chat_settings.filter(property="done", value="true"))
async def cq_chat_settings_done(query: types.CallbackQuery):
    await query.answer(_("Settings saved"), show_alert=True)
    await query.message.delete()
