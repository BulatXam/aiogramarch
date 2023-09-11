from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_game_durak(message: Message):
    await message.answer("Начинаем игру в дурака!")
