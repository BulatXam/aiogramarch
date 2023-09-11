from tortoise import fields

from src.core.orm.models import AbstractBaseModel
from src.core.orm.mixins import TimestampMixin


class AbstractUser(AbstractBaseModel, TimestampMixin):
    user_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=32)
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64)

    class Meta:
        abstract = True
