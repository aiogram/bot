from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.base_class import Base


class User(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True, unique=True)
    create_date = sa.Column(sa.DateTime(True), server_default=func.now())

    @classmethod
    def get_user(cls, db_session: Session, user_id: int) -> User:
        user = db_session.query(cls).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id)
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
        return user
