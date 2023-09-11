"""
    Сборник дефолтных миксинов
"""

from tortoise import fields


class TimestampMixin:
    """
    Миксин отметки времени создания/модификации.
    """

    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
