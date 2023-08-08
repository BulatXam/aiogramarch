from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .settings import settings


bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
