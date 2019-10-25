from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from app import config

DEFAULT = "default"

jobstores = {
    DEFAULT: RedisJobStore(
        db=config.REDIS_DB_JOBSTORE, host=config.REDIS_HOST, port=config.REDIS_PORT
    )
}
executors = {DEFAULT: AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 3600}

scheduler = AsyncIOScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc
)


async def on_startup(dispatcher: Dispatcher):
    scheduler.start()


async def on_shutdown(dispatcher: Dispatcher):
    scheduler.shutdown()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
