# Import all the models, so that Base has them before being
# imported by Alembic

from .base_class import Base
from .chat import Chat
from .user import User
