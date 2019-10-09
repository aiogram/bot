from aiogram import md, types
from aiogram.dispatcher.filters import CommandStart
from loguru import logger

from app.misc import dp


@dp.message_handler(CommandStart(), types.ChatType.is_private)
async def cmd_start(message: types.Message):
    logger.info("User {user} start conversation with bot", user=message.from_user.id)
    await message.answer(
        f"Hello, {md.hbold(message.from_user.full_name)}!\n"
        f"I'm <b>aiogram</b> bot.\n"
        f'My source code: <a href="https://github.com/aiogram/bot">github</a>'
    )
