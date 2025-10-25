from datetime import date as dt_date

from .callback_data import TargetDay


class TargetDayButton:
    def __init__(self, text: str, user_tg_id: int, button: str, date: dt_date, day: int | None = None):
        self.text = text
        self.callback_data = TargetDay(
            button=button,
            user_id=user_tg_id,
            year=int(date.year),
            month=int(date.month),
            day=day if day else int(date.day),
        )

    def as_kwargs(self):
        return self.__dict__
