""" Подключаем фильтры в базовый роутер """

from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from .models import Channel

from ...config import bot

from . import logs


class SubscribersFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        channels_ids = [channel.channel_id for channel in await Channel.all()]
        channels_statuses = []
        not_sub_channels = []

        for channel_id in channels_ids:
            user = await bot.get_chat_member(
                chat_id=channel_id,
                user_id=message.from_user.id,
            )
            if user.status == 'left':
                channels_statuses.append('left')
                not_sub_channels.append(channel_id)
            else:
                channels_statuses.append('notleft')

        if "left" in channels_statuses:
            await logs.not_sub(message, channels_ids=not_sub_channels)
        else:
            return True
