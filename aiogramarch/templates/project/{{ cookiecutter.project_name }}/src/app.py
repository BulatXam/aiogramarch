import asyncio
from loguru import logger

from src.core.bot_app import start_bot
from src.core.db import database_init

from .apps import models


async def start_app():
    logger.info("Main start app")

    await database_init(models=models)

    await asyncio.gather(
        start_bot()
    )
