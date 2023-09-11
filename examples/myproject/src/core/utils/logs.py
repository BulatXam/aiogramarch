"""
    Отправка логов в бота через сторонние сервисы
"""


async def send_logs(chat_id: int, text: str, parse_mode: str) -> None:
    from src.core.startapp import bot

    await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
