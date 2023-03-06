""" Сборка всех приложений проекта """

from aiogram import Router

from loguru import logger

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from .main.handlers import router as main_router

bot_routers = [main_router, {context.app_name}_router]


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

models = ["src.apps.main.models"]
