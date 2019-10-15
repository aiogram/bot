from _contextvars import ContextVar

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.orm import Session as SASession

from app.models.session import Session

DB_SESSION_KEY = "db_session"


class SQLAlchemySessionMiddleware(BaseMiddleware):
    session = ContextVar("SQLAlchemy-Session")

    async def on_pre_process_update(self, update: types.Update, data: dict):
        db_session = Session()
        self.session.set(db_session)

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        db_session = self.session.get()
        db_session.close()


def get_db() -> SASession:
    return SQLAlchemySessionMiddleware.session.get()
