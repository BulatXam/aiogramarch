from .settings import settings

from src.apps import models

TORTOISE_ORM = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models": {
            "models": [*models, "aerich.models"],
            "default_connection": "default",
        },
    },
}
