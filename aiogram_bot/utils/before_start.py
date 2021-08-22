import asyncio

import tenacity
from loguru import logger
from tenacity import _utils

from aiogram_bot import config
from aiogram_bot.models.db import db
from aiogram_bot.utils.redis import BaseRedis

TIMEOUT_BETWEEN_ATTEMPTS = 2
MAX_TIMEOUT = 30


def before_log(retry_state):
    if retry_state.outcome.failed:
        verb, value = "raised", retry_state.outcome.exception()
    else:
        verb, value = "returned", retry_state.outcome.result()

    logger.info(
        "Retrying {callback} in {sleep} seconds as it {verb} {value}",
        callback=_utils.get_callback_name(retry_state.fn),
        sleep=getattr(retry_state.next_action, "sleep"),
        verb=verb,
        value=value,
    )


def after_log(retry_state):
    logger.info(
        "Finished call to {callback!r} after {time:.2f}, this was the {attempt} time calling it.",
        callback=_utils.get_callback_name(retry_state.fn),
        time=retry_state.seconds_since_start,
        attempt=_utils.to_ordinal(retry_state.attempt_number),
    )


@tenacity.retry(
    wait=tenacity.wait_fixed(TIMEOUT_BETWEEN_ATTEMPTS),
    stop=tenacity.stop_after_delay(MAX_TIMEOUT),
    before_sleep=before_log,
    after=after_log,
)
async def wait_redis():
    connector = BaseRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
    try:
        await connector.connect()
        info = await connector.redis.info()
        logger.info("Connected to Redis server v{redis}", redis=info["server"]["redis_version"])
    finally:
        await connector.disconnect()


@tenacity.retry(
    wait=tenacity.wait_fixed(TIMEOUT_BETWEEN_ATTEMPTS),
    stop=tenacity.stop_after_delay(MAX_TIMEOUT),
    before_sleep=before_log,
    after=after_log,
)
async def wait_postgres():
    await db.set_bind(config.POSTGRES_URI)
    version = await db.scalar("SELECT version();")
    logger.info("Connected to {postgres}", postgres=version)


async def main():
    logger.info("Wait for RedisDB...")

    try:
        await wait_redis()
    except tenacity.RetryError:
        logger.error("Failed to establish connection with RedisDB.")
        exit(1)

    logger.info("Wait for PostgreSQL...")
    try:
        await wait_postgres()
    except tenacity.RetryError:
        logger.error("Failed to establish connection with PostgreSQL.")
        exit(1)
    logger.info("Ready.")


if __name__ == "__main__":
    asyncio.run(main())
