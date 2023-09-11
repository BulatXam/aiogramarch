""" Здесь находиться вся конфигурация. """

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import aioredis

from pathlib import Path

from .settings import settings

# <----                     Конфигурация aiogram                          ---->

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# <----                     Конфигурация fastapi                          ---->

fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# <----                   Конфигурация админки                        ---->



# <----                   Конфигурация базы данных                        ---->

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

redis = aioredis.Redis(host='localhost', port=6379, db=0)

BASE_DIR = Path.cwd()
CORE_DIR = Path(BASE_DIR / "src" / "core")
MEDIA_DIR = Path(CORE_DIR / "src" / "media")
STATIC_DIR = Path(CORE_DIR / "src" / "static")
