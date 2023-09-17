from typing import List

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def get_not_sub_keyboard(channels_ids: List[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=channel_id,
                url="https://t.me/"+channel_id.replace("@", "")
            )] for channel_id in channels_ids
        ]
    )
