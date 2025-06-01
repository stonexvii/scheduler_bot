from aiogram.filters.callback_data import CallbackData

from datetime import datetime


class TargetDay(CallbackData, prefix='TD'):
    button: str
    year: int
    month: int
    day: int
