import click
from aiogram.__main__ import SysInfo
from aiogram.utils import executor
from loguru import logger

from app import logging
from app.misc import dp


@click.group()
def cli():
    logging.setup()

    # noinspection PyUnresolvedReferences
    import app.handlers


@cli.command()
def version():
    logger.info(SysInfo())


@cli.command()
def polling():
    executor.start_polling(dp)
