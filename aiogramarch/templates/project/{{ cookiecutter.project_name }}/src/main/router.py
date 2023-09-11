from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Text

from . import logs


router = Router(name="main")


@router.message(
    Text("/start"), F.chat.type == 'private'
)
async def profile(message: Message):
    pass
