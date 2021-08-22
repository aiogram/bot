import datetime
import time
from contextlib import suppress
from typing import List

from aiogram import Dispatcher
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.utils.executor import Executor
from loguru import logger

from aiogram_bot import config
from aiogram_bot.misc import bot
from aiogram_bot.services.apscheduller import scheduler
from aiogram_bot.utils.redis import BaseRedis

JOB_PREFIX = "join_list_cleaner"


class JoinListService(BaseRedis):
    def __init__(self, prefix="chat", *args, **kwargs):
        super(JoinListService, self).__init__(*args, **kwargs)
        self.prefix = prefix

    def create_key(self, chat_id: int, message_id: int) -> str:
        return f"{self.prefix}:{chat_id}:{message_id}"

    async def create_list(self, chat_id: int, message_id: int, users: List[int]):
        key = self.create_key(chat_id=chat_id, message_id=message_id)
        for user_id in users:
            score = time.time()
            logger.info("Add user to join-list {key} {value}", key=key, score=score, value=user_id)
            await self.redis.zadd(key, score, user_id)
        scheduler.add_job(
            join_expired,
            "date",
            id=f"{JOB_PREFIX}:{chat_id}:{message_id}",
            run_date=datetime.datetime.utcnow() + config.JOIN_CONFIRM_DURATION,
            kwargs={"chat_id": chat_id, "message_id": message_id},
        )

    async def pop_user_from_list(self, chat_id: int, message_id: int, user_id: int):
        key = self.create_key(chat_id=chat_id, message_id=message_id)
        in_list = await self.redis.zrem(key, user_id)
        if in_list:
            logger.info("Remove user from join-list {key} {user_id}", key=key, user_id=user_id)
        return in_list

    async def check_list(self, chat_id: int, message_id: int) -> List[int]:
        key = self.create_key(chat_id=chat_id, message_id=message_id)
        users_list = await self.redis.zrange(key)
        return list(map(int, users_list))


async def join_expired(chat_id: int, message_id: int):
    users = await join_list.check_list(chat_id=chat_id, message_id=message_id)
    if not users:
        logger.info(
            "All users from join-list in chat {chat} and message {message} already answer for question",
            chat=chat_id,
            message=message_id,
        )
        return

    for user_id in users:
        await join_list.pop_user_from_list(chat_id=chat_id, message_id=message_id, user_id=user_id)
        logger.info(
            "Kick chat member {user} from chat {chat} "
            "in due to user do not answer to the question in message {message}.",
            user=user_id,
            chat=chat_id,
            message=message_id,
        )
        await bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
        await bot.unban_chat_member(chat_id=chat_id, user_id=user_id)

    with suppress(MessageToDeleteNotFound):
        await bot.delete_message(chat_id, message_id)


join_list = JoinListService(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB_JOIN_LIST
)


async def on_startup(dispatcher: Dispatcher):
    await join_list.connect()


async def on_shutdown(dispatcher: Dispatcher):
    await join_list.disconnect()


def setup(runner: Executor):
    runner.on_startup(on_startup)
    runner.on_shutdown(on_shutdown)
