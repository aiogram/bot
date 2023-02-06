from typing import Any, Dict
from urllib.parse import urljoin

from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from aiohttp import ClientSession

from aiogram_bot import config


class HasteBinClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = ClientSession()

    def format_url(self, uri: str) -> str:
        return urljoin(self.base_url, uri)

    async def create_document(self, content: bytes) -> Dict[str, Any]:
        response = await self.session.post(url=self.format_url("/documents"), data=content)
        response.raise_for_status()
        return await response.json()


hastebin = HasteBinClient(config.HASTEBIN_URL)


async def on_startup(dispatcher: Dispatcher):
    pass


async def on_shutdown(dispatcher: Dispatcher):
    await hastebin.session.close()


def setup(runner: Executor):
    runner.on_startup(on_startup)
    runner.on_shutdown(on_shutdown)
