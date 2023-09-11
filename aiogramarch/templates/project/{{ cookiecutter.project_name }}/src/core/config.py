""" Здесь находиться вся конфигурация """

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from pathlib import Path

from .settings import settings

# <----                            Aiogram                                ---->

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# <----                           Fastapi                                 ---->


# <----                           Админка                                 ---->


# <----                         База данных                               ---->

TORTOISE_ORM = lambda models: {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models": {
            "models": [*models, "src.core.admin.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# <----                   Константы, неизменяемые данные                  ----> 

BASE_DIR = Path.cwd()
CORE_DIR = Path(BASE_DIR / "src" / "core")
MEDIA_DIR = Path(CORE_DIR / "media")
STATIC_DIR = Path(CORE_DIR / "static")
