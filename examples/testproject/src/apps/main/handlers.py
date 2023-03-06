from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="Main")


@router.message(Command('start'))
async def start(message: Message):
    await message.answer("СТАРТУЕМ!!!11!!1")
