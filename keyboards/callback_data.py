from aiogram.filters.callback_data import CallbackData


class TargetDay(CallbackData, prefix='TD'):
    button: str
    year: int
    month: int
    day: int
    option: int = 0
