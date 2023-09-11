"""
    Сборник дефолтных моделей
"""

from tortoise import fields
from tortoise.models import Model


class AbstractBaseModel(Model):
    """
    Главная абстрактная модель с перманентым ключем
    """

    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
