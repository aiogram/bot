from __future__ import annotations

from sqlalchemy.sql import expression

from aiogram_bot.models.db import BaseModel, TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True, index=True, unique=True)

    is_superuser = db.Column(db.Boolean, server_default=expression.false())
    start_conversation = db.Column(db.Boolean, server_default=expression.false())
    do_not_disturb = db.Column(
        db.Boolean, default=False, server_default=expression.false(), nullable=False
    )


class UserRelatedModel(BaseModel):
    __abstract__ = True

    user_id = db.Column(
        db.ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
