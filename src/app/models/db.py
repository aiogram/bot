import datetime

import sqlalchemy as sa
from gino import Gino
from sqlalchemy import func

from app import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
    )


async def on_startup(_):
    await db.set_bind(f"asyncpg://{config.POSTGRES_URI}")
