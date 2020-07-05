from .chat import ChatRelatedModel
from .db import TimedBaseModel, db
from .user import UserRelatedModel


class BlackListWord(TimedBaseModel, ChatRelatedModel, UserRelatedModel):
    __tablename__ = "words_blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.VARCHAR(4096))
