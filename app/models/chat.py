from sqlalchemy.sql import expression

from app.models.db import BaseModel, TimedBaseModel, db


class Chat(TimedBaseModel):
    __tablename__ = "chats"

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    type = db.Column(db.String)
    is_official = db.Column(db.Boolean, server_default=expression.false())

    language = db.Column(db.String(12), default="en")
    join_filter = db.Column(db.Boolean, server_default=expression.false())


class ChatRelatedModel(BaseModel):
    __abstract__ = True

    chat_id = db.Column(
        db.ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
