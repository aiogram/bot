import click
from aiogram.__main__ import SysInfo
from aiogram.utils import executor
from loguru import logger


@click.group()
def cli():
    from app.utils import logging
    from app import misc

    logging.setup()
    misc.setup()


@cli.command()
def version():
    """
    Get application version

    :return:
    """
    click.echo(SysInfo())


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
@click.option(
    "--autoreload", is_flag=True, default=False, help="Reload application on file changes"
)
def polling(skip_updates: bool, autoreload: bool):
    """
    Application runner in polling mode

    :param skip_updates: Skip pending updates
    :param autoreload: autoreload application on file changes
    """
    from app.misc import dp

    if autoreload:
        import aiohttp_autoreload

        logger.warning("Application started in live-reload mode. Please disable it in production!")
        aiohttp_autoreload.start()

    executor.start_polling(dp, skip_updates=skip_updates)
