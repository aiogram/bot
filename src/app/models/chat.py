from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.base_class import Base


class Chat(Base):
    id = sa.Column(sa.BigInteger, primary_key=True, index=True)
    language = sa.Column(sa.String(12), default="en")
    create_date = sa.Column(sa.DateTime(True), server_default=func.now())

    @classmethod
    def get_chat(cls, db_session: Session, chat_id: int):
        chat = db_session.query(cls).filter(cls.id == chat_id).first()
        if not chat:
            chat = Chat(id=chat_id)
            db_session.add(chat)
            db_session.commit()
            db_session.refresh(chat)
        return chat
