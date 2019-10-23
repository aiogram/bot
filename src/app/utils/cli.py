import click
from aiogram.__main__ import SysInfo
from loguru import logger

try:
    import aiohttp_autoreload
except ImportError:
    aiohttp_autoreload = None


@click.group()
@click.option(
    "--autoreload", is_flag=True, default=False, help="Reload application on file changes"
)
def cli(autoreload: bool):
    if autoreload and aiohttp_autoreload:
        logger.warning("Application started in live-reload mode. Please disable it in production!")
        aiohttp_autoreload.start()
    elif autoreload and not aiohttp_autoreload:
        click.echo("`aiohttp_autoreload` is not installed.", err=True)

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
def polling(skip_updates: bool):
    """
    Application runner in polling mode

    :param skip_updates: Skip pending updates
    """

    from app.utils.executor import runner

    runner.skip_updates = skip_updates
    runner.start_polling(reset_webhook=True)


@cli.command()
def webhook():
    from app.utils.executor import runner
    from app import config

    runner.start_webhook(webhook_path=config.WEBHOOK_PATH, port=config.BOT_PUBLIC_PORT)
