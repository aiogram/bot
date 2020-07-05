from aiogram import types

from app.misc import i18n
from app.models.blacklist_word import BlackListWord
from app.models.db import db

_ = i18n.gettext

WORDS_PER_PAGE = 15


async def build_blacklist_page(chat_id: int, page: int = 0):
    offset = page * WORDS_PER_PAGE

    query = BlackListWord.query.where(BlackListWord.chat_id == chat_id)

    words = await query.limit(WORDS_PER_PAGE).offset(offset).gino.all()
    total_count = (
        await db.func.count(BlackListWord.id).where(BlackListWord.chat_id == chat_id).gino.scalar()
    )
    print(total_count)

    markup = types.InlineKeyboardMarkup()
    for word in words:  # type: BlackListWord
        markup.add(
            types.InlineKeyboardButton(word.word, callback_data="placeholder"),
            types.InlineKeyboardButton(_("delete word"), callback_data="placeholder"),
        )
    markup.add(types.InlineKeyboardButton(_("Add more"), callback_data="placeholder"))

    return "test", markup
