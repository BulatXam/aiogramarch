from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Text


router = Router(name="user")


@router.message(
    Text("/start"), F.chat.type == 'private'
)
async def profile(message: Message):
    pass
