""" Сборка переменных окружения из dotenv """

from pydantic import BaseSettings
from pydantic.error_wrappers import ValidationError

class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_URL: str

    AIOGRAM_PROJECT_NAME: str
    AIOGRAM_PROJECT_DIR: str
    AIOGRAM_PROJECT_APPS_DIR: str

    class Config:
        case_sensitive = True
        env_file = "env.env"


try:
    settings = Settings()
except ValidationError:
    settings = Settings(
        BOT_TOKEN="",
        DB_URL="",
        AIOGRAM_PROJECT_NAME="",
        AIOGRAM_PROJECT_DIR="",
        AIOGRAM_PROJECT_APPS_DIR="",
    )
