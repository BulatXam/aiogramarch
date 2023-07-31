""" Сборка бота """
from loguru import logger


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .settings import settings

from ..apps import bot_base_router


bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def start_bot():
    # include routers
    logger.info("Include base_router")
    dp.include_router(bot_base_router)

    logger.info("Start polling")
    await dp.start_polling(bot)
