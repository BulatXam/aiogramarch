from aiogram.filters.callback_data import CallbackData

class ActionCallback(CallbackData, prefix="action"):
    action: str
