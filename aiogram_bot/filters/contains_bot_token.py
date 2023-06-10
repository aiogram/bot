import re
import typing
from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class ContainsBotToken(BoundFilter):
    """
    Filtered message should contain working token for Telegram bot
    """

    key = "contains_bot_token"

    token_regex = re.compile(r"(\d{0,16}:[a-zA-Z0-9_\-]{35})")

    async def check(self, message: types.Message) -> typing.Union[bool, typing.Dict[str, str]]:
        txt = message.text or message.caption
        result = self.token_regex.search(txt)
        if result is None:
            return False
        return {"token": result.group(0)}
