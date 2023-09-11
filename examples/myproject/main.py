import asyncio

from src.core import run, TORTOISE_ORM

from src import models, fastapi_routers, bot_base_router

TORTOISE_ORM = TORTOISE_ORM(models=models)

asyncio.run(
    run(
        tortoise_orm=TORTOISE_ORM,
        fastapi_routers=fastapi_routers,
        bot_base_router=bot_base_router,
    )
)
