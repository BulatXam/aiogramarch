import sys

from loguru import logger

from importlib import import_module
from dotenv import load_dotenv

from .database import database_init
from ..config import (
    get_project_base_dir,
    get_project_name
)

async def close() -> None:
    from tortoise.connection import connections

    await connections.close_all(discard=True)


async def run() -> None:
    """
    Функция, работающая в корневой папке проекта и запускается в корневой папке

    """
    from .bot import bot, dp

    project_base_dir = get_project_base_dir()
    load_dotenv(project_base_dir / "env.env")

    project_name = get_project_name()
    apps_module = import_module(package=f"{project_name}", name="src")


    await database_init(
        apps_module.TORTOISE_ORM
    )

    logger.info("Include base_router")
    dp.include_router(apps_module.bot_base_router)

    logger.info("Start polling")

    try:
        await dp.start_polling(bot)
    finally:
        await close()
