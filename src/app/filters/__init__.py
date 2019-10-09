from aiogram import Dispatcher

from app.filters.has_permissions import BotHasPermissions


def setup(dispatcher: Dispatcher):
    from .is_reply import IsReplyFilter
    from .has_permissions import HasPermissions

    text_messages = [
        dispatcher.message_handlers,
        dispatcher.edited_message_handlers,
        dispatcher.channel_post_handlers,
        dispatcher.edited_channel_post_handlers,
    ]

    dispatcher.filters_factory.bind(IsReplyFilter, event_handlers=text_messages)
    dispatcher.filters_factory.bind(HasPermissions, event_handlers=text_messages)
    dispatcher.filters_factory.bind(BotHasPermissions, event_handlers=text_messages)
