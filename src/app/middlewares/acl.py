from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.middlewares.db import get_db
from app.models.chat import Chat
from app.models.user import User


class ACLMiddleware(BaseMiddleware):
    def setup_chat(self, data: dict, user: types.User, chat: Optional[types.Chat] = None):
        session = get_db()
        data["user"] = User.get_user(session, user.id)
        if chat:
            data["chat"] = Chat.get_chat(session, chat.id)
        else:
            data["chat"] = Chat.get_chat(session, user.id)

    async def on_pre_process_message(self, message: types.Message, data: dict):
        self.setup_chat(data, message.from_user, message.chat)
