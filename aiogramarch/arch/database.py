""" Сборка базы данных """

from typing import List

from tortoise import Tortoise
from loguru import logger


async def database_init(tortoise_settings: dict) -> None:
    """
    Initialises ORM.
    """
    logger.debug("Init db")

    await Tortoise.init(tortoise_settings)
    await Tortoise.generate_schemas()
