import functools

import click
from aiogram.__main__ import SysInfo
from loguru import logger

try:
    import aiohttp_autoreload
except ImportError:
    aiohttp_autoreload = None


@click.group()
def cli():
    from aiogram_bot import misc
    from aiogram_bot.utils import logging

    logging.setup()
    misc.setup()


def auto_reload_mixin(func):
    @click.option(
        "--autoreload", is_flag=True, default=False, help="Reload application on file changes"
    )
    @functools.wraps(func)
    def wrapper(autoreload: bool, *args, **kwargs):
        if autoreload and aiohttp_autoreload:
            logger.warning(
                "Application started in live-reload mode. Please disable it in production!"
            )
            aiohttp_autoreload.start()
        elif autoreload and not aiohttp_autoreload:
            click.echo("`aiohttp_autoreload` is not installed.", err=True)
        return func(*args, **kwargs)

    return wrapper


@cli.command()
def version():
    """
    Get application version
    """
    click.echo(SysInfo())


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
@auto_reload_mixin
def polling(skip_updates: bool):
    """
    Start application in polling mode
    """

    from aiogram_bot.utils.executor import runner

    runner.skip_updates = skip_updates
    runner.start_polling(reset_webhook=True)


@cli.command()
@auto_reload_mixin
def webhook():
    """
    Run application in webhook mode
    """
    from aiogram_bot import config
    from aiogram_bot.utils.executor import runner

    runner.start_webhook(webhook_path=config.WEBHOOK_PATH, port=config.BOT_PUBLIC_PORT)


@cli.command()
@click.argument("user_id", type=int)
@click.option("--remove", "--rm", is_flag=True, default=False, help="Remove superuser rights")
def superuser(user_id: int, remove: bool):
    from aiogram_bot.utils.executor import runner
    from aiogram_bot.utils.superuser import create_super_user

    try:
        result = runner.start(create_super_user(user_id, remove))
    except Exception as e:
        logger.exception("Failed to create superuser: {e}", e=e)
        result = None

    if not result:
        exit(1)
