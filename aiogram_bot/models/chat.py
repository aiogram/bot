from sqlalchemy.sql import expression

from aiogram_bot.models.db import BaseModel, TimedBaseModel, db


class Chat(TimedBaseModel):
    __tablename__ = "chats"

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    type = db.Column(db.String)
    is_official = db.Column(db.Boolean, server_default=expression.false())

    language = db.Column(db.String(12), default="en")
    join_filter = db.Column(db.Boolean, server_default=expression.false())
    ban_channels = db.Column(db.Boolean, server_default=expression.false())
    delete_channel_messages = db.Column(db.Boolean, server_default=expression.false())
    report_to_admins = db.Column(db.Boolean, server_default=expression.true())
    restrict_commands = db.Column(db.Boolean, server_default=expression.true())


class ChatRelatedModel(BaseModel):
    __abstract__ = True

    chat_id = db.Column(
        db.ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )


class ChatAllowedChannels(TimedBaseModel):
    __tablename__ = "chats_allowed_channels"

    chat_id = db.Column(
        db.ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    channel_id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    added_by = db.Column(
        db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
