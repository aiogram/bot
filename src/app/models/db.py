import datetime

from gino import Gino

from app import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
    )


async def on_startup(_):
    await db.set_bind(config.POSTGRES_URI)
