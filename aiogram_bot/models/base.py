# Import all the models, so that Base has them before being
# imported by Alembic

from .chat import Chat, ChatAllowedChannels
from .db import db
from .user import User

__all__ = (
    "db",
    "Chat",
    "ChatAllowedChannels",
    "User",
)
