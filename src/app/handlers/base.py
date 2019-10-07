from aiogram import md, types
from aiogram.dispatcher.filters import CommandStart

from app.misc import dp


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Hello, {md.quote_html(message.from_user.full_name)}!")
