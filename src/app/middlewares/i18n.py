from typing import Any, Tuple

from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware


class I18nMiddleware(BaseI18nMiddleware):
    AVAILABLE_LANGUAGES = ["en", "ru", "uk"]

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        data: dict = args[-1]
        if "chat" in data:
            return data["chat"].language or self.default
        return self.default
