import datetime
from typing import List

import sqlalchemy as sa
from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from gino import Gino
from loguru import logger

from aiogram_bot import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


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
