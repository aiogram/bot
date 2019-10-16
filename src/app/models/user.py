from __future__ import annotations

import sqlalchemy as sa

from app.models.db import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True, unique=True)
