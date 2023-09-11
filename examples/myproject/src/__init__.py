""" Импорт необходимых данных приложений для сборки бота """

from aiogram import Router

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from fastapi import APIRouter

from loguru import logger
from typing import List

from .user.admin import *

from .admin.api import router as admin_fastapi_router


models = ["src.user.models"]

bot_routers: List[Router] = []
fastapi_routers: List[APIRouter] = [admin_fastapi_router]

bot_base_router = Router(name="base_router")


@bot_base_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply('На данный момент нет никакого state!')
        return

    await state.clear()
    await message.reply('Вы отменили state!')


for router in bot_routers:
    logger.info(f"Include router: {router.__str__()}")
    bot_base_router.include_router(router)
