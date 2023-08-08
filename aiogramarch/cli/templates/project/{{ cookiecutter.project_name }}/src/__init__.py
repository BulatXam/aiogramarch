""" Сборка всех приложений проекта """

from aiogram import Router

from loguru import logger

from pathlib import Path

from pydantic import error_wrappers as pydantic_eror_wrappers

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


try:
    from aiogramarch import settings
except pydantic_eror_wrappers.ValidationError:
    # Если необходимо получить содержимое отдельно от проекта.
    logger.debug("Мы не смогли получить env")
    pass


bot_routers = []
models = []


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


TORTOISE_ORM = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models": {
            "models": [*models, "aerich.models"],
            "default_connection": "default",
        },
    },
}

# <----                                                                   ---->
#                         Здесь данные админки
# <----                                                                   ----> 


# <----                                                                   ---->
#                      Здесь данные медиа-данных
# <----                                                                   ----> 


# <----                                                                   ---->
#                    Здесь данные статических данных
# <----                                                                   ----> 
