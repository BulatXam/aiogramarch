""" Сборка переменных окружения из dotenv """

from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_URL: str

    class Config:
        case_sensitive = True
        env_file = "~/env.env"


settings = Settings()
