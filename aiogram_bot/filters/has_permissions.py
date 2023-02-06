import typing
from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import Filter


@dataclass
class HasPermissions(Filter):
    """
    Validate the user has specified permissions in chat
    """

    can_post_messages: bool = False
    can_edit_messages: bool = False
    can_delete_messages: bool = False
    can_restrict_members: bool = False
    can_promote_members: bool = False
    can_change_info: bool = False
    can_invite_users: bool = False
    can_pin_messages: bool = False

    ARGUMENTS = {
        "user_can_post_messages": "can_post_messages",
        "user_can_edit_messages": "can_edit_messages",
        "user_can_delete_messages": "can_delete_messages",
        "user_can_restrict_members": "can_restrict_members",
        "user_can_promote_members": "can_promote_members",
        "user_can_change_info": "can_change_info",
        "user_can_invite_users": "can_invite_users",
        "user_can_pin_messages": "can_pin_messages",
    }
    PAYLOAD_ARGUMENT_NAME = "user_member"

    def __post_init__(self):
        self.required_permissions = {
            arg: True for arg in self.ARGUMENTS.values() if getattr(self, arg)
        }

    @classmethod
    def validate(
        cls, full_config: typing.Dict[str, typing.Any]
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        config = {}
        for alias, argument in cls.ARGUMENTS.items():
            if alias in full_config:
                config[argument] = full_config.pop(alias)
        return config

    def _get_cached_value(self, message: types.Message):
        try:
            return message.conf[self.PAYLOAD_ARGUMENT_NAME]
        except KeyError:
            return None

    def _set_cached_value(self, message: types.Message, member: types.ChatMember):
        message.conf[self.PAYLOAD_ARGUMENT_NAME] = member

    async def _get_chat_member(self, message: types.Message):
        chat_member: types.ChatMember = self._get_cached_value(message)
        if chat_member is None:
            admins = await message.chat.get_administrators()
            target_user_id = await self.get_target_id(message)
            try:
                chat_member = next(filter(lambda member: member.user.id == target_user_id, admins))
            except StopIteration:
                return False
            self._set_cached_value(message, chat_member)
        return chat_member

    async def check(
        self, message: types.Message
    ) -> typing.Union[bool, typing.Dict[str, typing.Any]]:
        chat_member = await self._get_chat_member(message)
        if not chat_member:
            return False
        if chat_member.status == types.ChatMemberStatus.CREATOR:
            return chat_member
        for permission, value in self.required_permissions.items():
            if not getattr(chat_member, permission):
                return False

        return {self.PAYLOAD_ARGUMENT_NAME: chat_member}

    async def get_target_id(self, message: types.Message) -> int:
        return message.from_user.id


class BotHasPermissions(HasPermissions):
    """
    Validate the bot has permissions in chat
    """

    ARGUMENTS = {
        "bot_can_post_messages": "can_post_messages",
        "bot_can_edit_messages": "can_edit_messages",
        "bot_can_delete_messages": "can_delete_messages",
        "bot_can_restrict_members": "can_restrict_members",
        "bot_can_promote_members": "can_promote_members",
        "bot_can_change_info": "can_change_info",
        "bot_can_invite_users": "can_invite_users",
        "bot_can_pin_messages": "can_pin_messages",
    }
    PAYLOAD_ARGUMENT_NAME = "bot_member"

    async def get_target_id(self, message: types.Message) -> int:
        return (await message.bot.me).id
