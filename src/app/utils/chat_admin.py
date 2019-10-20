from typing import Optional

from aiogram.types import ChatMember

from app.misc import bot


async def get_chat_administrator(chat_id: int, user_id: int) -> Optional[ChatMember]:
    admins = await bot.get_chat_administrators(chat_id)
    try:
        return next(filter(lambda member: member.user.id == user_id, admins))
    except StopIteration:
        return None
