from tortoise import fields

from ...orm.mixins import TimestampMixin
from ...orm.models import AbstractBaseModel


class Channel(AbstractBaseModel, TimestampMixin):
    channel_id = fields.CharField(max_length=300)
