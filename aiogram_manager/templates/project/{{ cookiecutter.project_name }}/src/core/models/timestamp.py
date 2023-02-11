"""
    Mixin for `created at`, `modified at` fields.
"""

from tortoise import fields


class TimestampMixin:
    """
    Mixin that adds two fields with `created` / `modified` at timestamps.
    """

    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
