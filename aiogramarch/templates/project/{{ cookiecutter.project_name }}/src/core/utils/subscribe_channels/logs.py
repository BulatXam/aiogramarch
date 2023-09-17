from typing import List

from aiogram.types import Message

from . import keyboards


async def not_sub(message: Message, channels_ids: List[str]) -> None:
    await message.answer(
        text=f'❌<b>ТЫ НЕ ПОДПИСАН НА КАНАЛЫ!</b>❌\n\n'
                f'<i>Подпишись на канал, '
                f'что бы получить доступ к боту!</i>',
        parse_mode='HTML',
        reply_markup=keyboards.get_not_sub_keyboard(channels_ids=channels_ids)
    )
