""" Сборка базы данных """

from tortoise import Tortoise
from tortoise.connection import connections

from loguru import logger


async def database_connections_close() -> None:
    logger.debug("Database connections close")
    await connections.close_all(discard=True)


async def database_init(tortoise_orm: dict) -> None:
    """
    Initialises ORM.
    """
    logger.debug("Init db")

    await Tortoise.init(tortoise_orm)
    await Tortoise.generate_schemas()
