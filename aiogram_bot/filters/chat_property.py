from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from aiogram_bot.models.chat import Chat


@dataclass
class ChatPropertyFilter(BoundFilter):
    key = "chat_property"
    chat_property: str

    async def check(self, obj) -> bool:
        data = ctx_data.get()
        chat: Chat = data["chat"]
        return getattr(chat, self.chat_property, False)
