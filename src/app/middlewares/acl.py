from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.models.chat import Chat
from app.models.user import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User, chat: Optional[types.Chat] = None):
        user_id = user.id
        chat_id = chat.id if chat else user.id

        user = await User.get(user_id)
        if user is None:
            user = await User.create(id=user_id)
        chat = await Chat.get(chat_id)
        if chat is None:
            chat = await Chat.create(id=chat_id)

        data["user"] = user
        data["chat"] = chat

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message.chat)
