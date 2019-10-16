from __future__ import annotations

import sqlalchemy as sa

from app.models.db import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    id = sa.Column(sa.BigInteger, primary_key=True, index=True)
    type = sa.Column(sa.String)
    language = sa.Column(sa.String(12), default="en")
