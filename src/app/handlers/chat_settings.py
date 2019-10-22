from contextlib import suppress
from functools import partial

from aiogram import types
from aiogram.dispatcher.filters.filters import OrFilter
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageNotModified
from loguru import logger

from app.misc import bot, dp, i18n
from app.models.chat import Chat
from app.models.user import User
from app.utils.chat_admin import get_chat_administrator
from app.utils.chat_settings import (
    cb_chat_settings,
    cb_user_settings,
    get_chat_settings_markup,
    get_user_settings_markup,
)

_ = i18n.gettext


@dp.message_handler(
    types.ChatType.is_group_or_super_group, commands=["settings"], user_can_change_info=True
)
@dp.message_handler(types.ChatType.is_private, commands=["settings"])
async def cmd_chat_settings(message: types.Message, chat: Chat, user: User):
    logger.info("User {user} wants to configure chat {chat}", user=user.id, chat=chat.id)
    with suppress(MessageCantBeDeleted):
        await message.delete()

    if types.ChatType.is_private(message.chat):
        text, markup = get_user_settings_markup(chat, user)
    else:
        text, markup = get_chat_settings_markup(message.chat, chat)
    await bot.send_message(chat_id=user.id, text=text, reply_markup=markup)


@dp.callback_query_handler(cb_chat_settings.filter(property="language", value="change"))
@dp.callback_query_handler(cb_user_settings.filter(property="language", value="change"))
async def cq_chat_settings_language(query: types.CallbackQuery, chat: Chat, callback_data: dict):
    if callback_data["@"] == "chat":
        target_chat_id = int(callback_data["id"])
        chat = await Chat.query.where(Chat.id == target_chat_id).gino.first()
        if not chat:
            return await query.answer(_("Invalid chat"), show_alert=True)
        callback_factory = partial(cb_chat_settings.new, id=chat.id)
    else:
        callback_factory = cb_user_settings.new

    markup = types.InlineKeyboardMarkup()

    for code, language in i18n.AVAILABLE_LANGUAGES.items():
        markup.add(
            types.InlineKeyboardButton(
                language.label, callback_data=callback_factory(property="language", value=code)
            )
        )

    await query.answer(_("Choose chat language"))
    await query.message.edit_reply_markup(markup)


@dp.callback_query_handler(
    OrFilter(
        *[
            cb_settings.filter(property="language", value=code)
            for code in i18n.AVAILABLE_LANGUAGES
            for cb_settings in [cb_chat_settings, cb_user_settings]
        ]
    )
)
async def cq_chat_settings_choose_language(
    query: types.CallbackQuery, chat: Chat, user: User, callback_data: dict
):
    target_language = callback_data["value"]

    if callback_data["@"] == "chat":
        target_chat_id = int(callback_data["id"])
        chat = await Chat.query.where(Chat.id == target_chat_id).gino.first()
        if not chat:
            return await query.answer(_("Invalid chat"), show_alert=True)

        member = await get_chat_administrator(chat.id, query.message.from_user.id)
        if not member or not member.is_chat_admin():
            await query.answer(_("You cannot change settings of this chat!"), show_alert=True)
            return await query.message.delete()
    else:
        target_chat_id = None

    await chat.update(language=target_language).apply()
    await query.answer(
        _("Language changed to {new_language}").format(
            new_language=i18n.AVAILABLE_LANGUAGES[target_language].title
        )
    )
    if callback_data["@"] == "chat":
        text, markup = get_chat_settings_markup(await bot.get_chat(target_chat_id), chat)
    else:
        i18n.ctx_locale.set(target_language)
        text, markup = get_user_settings_markup(chat, user)
    await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(cb_user_settings.filter(property="do_not_disturb", value="switch"))
async def cq_user_settings_do_not_disturb(query: types.CallbackQuery, user: User, chat: Chat):
    await query.answer(_("Do not disturb mode reconfigured"))
    await user.update(do_not_disturb=~User.do_not_disturb).apply()
    text, markup = get_user_settings_markup(chat, user)
    with suppress(MessageNotModified):
        await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(cb_chat_settings.filter(property="done", value="true"))
@dp.callback_query_handler(cb_user_settings.filter(property="done", value="true"))
async def cq_chat_settings_done(query: types.CallbackQuery):
    await query.answer(_("Settings saved"), show_alert=True)
    await query.message.delete()
