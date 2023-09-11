from aiogram.types import Message


async def start_message(message: Message) -> None:
    await message.answer(
        text=None
)
