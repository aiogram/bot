from aiogram import types

from app.misc import dp, i18n
from app.utils.superuser import create_super_user

_ = i18n.gettext


@dp.message_handler(commands=["set_superuser"], commands_prefix="!", is_superuser=True)
async def cmd_superuser(message: types.Message):
    args = message.text.partition(" ")[2]
    if not args or not args[0].isdigit():
        return False
    args = args.split()
    user_id = int(args[0])
    remove = len(args) == 2 and args[1] == "-rm"

    try:
        result = await create_super_user(user_id=user_id, remove=remove)
    except ValueError:
        result = False

    if result:
        return await message.answer(
            _("Successful changed is_superuser to {is_superuser} for user {user}").format(
                is_superuser=not remove, user=user_id
            )
        )
    return await message.answer(
        _("Failed to set is_superuser to {is_superuser} for user {user}").format(
            is_superuser=not remove, user=user_id
        )
    )
