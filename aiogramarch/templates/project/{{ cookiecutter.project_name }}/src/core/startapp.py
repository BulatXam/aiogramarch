import asyncio

from aiogram import Router

from loguru import logger
from dotenv import load_dotenv
from pathlib import Path

from .config import bot, dp

from .database.core import database_init, database_connections_close


async def _start_bot(bot_base_router: Router) -> None:
    logger.info("Include bot base_router")
    dp.include_router(bot_base_router)

    logger.info("Start bot polling")

    await dp.start_polling(bot)


async def _start_app(
    bot_base_router: Router,
) -> None:
    await asyncio.gather(
        _start_bot(bot_base_router=bot_base_router)
    )


async def run(
    bot_base_router: Router,
    tortoise_orm: dict,
) -> None:
    """
    Функция, работающая в корневой папке проекта в main.py (ЭТО ЖИЗНЕННО ВАЖНО!)

    """
    load_dotenv(Path.cwd() / "env.env")

    await database_init(tortoise_orm=tortoise_orm)

    try:
        await _start_app(
            bot_base_router=bot_base_router,
            tortoise_orm=tortoise_orm
        )
    finally:
        await database_connections_close()
