from tortoise import fields
from tortoise.models import Model

from ..core.contrib.user.models import AbstractUser


class User(AbstractUser):
    """ Telegram client-user """
