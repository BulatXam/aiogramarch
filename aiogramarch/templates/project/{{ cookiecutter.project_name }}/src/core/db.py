""" Сборка базы данных """

from typing import List

from tortoise import Tortoise
from loguru import logger

from .settings import settings
#from sshtunnel import SSHTunnelForwarder


async def database_init(models: List[str]) -> None:
    """
    Initialises ORM.
    """
    logger.debug("Init db")

    TORTOISE_ORM = {
        "connections": {"default": settings.DB_URL},
        "apps": {
            "models": {
                "models": [*models, "aerich.models"],
                "default_connection": "default",
            },
        },
    }

    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()

