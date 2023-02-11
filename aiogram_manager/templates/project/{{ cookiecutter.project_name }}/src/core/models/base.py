"""
    Abstract Tortoise base model with default primary key ID.
"""

from tortoise import fields
from tortoise.models import Model


class AbstractBaseModel(Model):
    """
    Encapsulates realisation of the ID field.
    """

    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"
