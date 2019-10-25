import datetime

from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from gino import Gino
from loguru import logger

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


async def on_startup(dispatcher: Dispatcher):
    logger.info("Setup PostgreSQL Connection")
    await db.set_bind(config.POSTGRES_URI)


async def on_shutdown(dispatcher: Dispatcher):
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
