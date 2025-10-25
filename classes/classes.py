import calendar
from collections import namedtuple
from datetime import date, timedelta

from database.requests import get_month

Month = namedtuple('Month', ['main', 'alt'])


class EventCalendar:
    MONTHS = (
        '',
        Month('Январь', 'января'),
        Month('Февраль', 'февраля'),
        Month('Март', 'марта'),
        Month('Апрель', 'апреля'),
        Month('Май', 'мая'),
        Month('Июнь', 'июня'),
        Month('Июль', 'июля'),
        Month('Август', 'августа'),
        Month('Сентябрь', 'сентября'),
        Month('Октябрь', 'октября'),
        Month('Ноябрь', 'ноября'),
        Month('Декабрь', 'декабря'),
    )

    def __init__(self, current_date: date):
        self.date = current_date
        self.year = current_date.year
        self.month = current_date.month
        self._first_day = current_date.replace(day=1)

    def days_buttons(self) -> list:
        buttons = calendar.monthcalendar(self.year, self.month)
        return buttons

    def prev_next(self) -> tuple[date, date]:
        previous_month = (self._first_day - timedelta(days=1)).replace(day=1)
        next_month = (self._first_day + timedelta(days=31)).replace(day=1)
        return previous_month, next_month

    async def busy_days(self, user_id: int):
        events = await get_month(user_id, self.date)
        events = {event.date.day for event in events}
        return events

    def __str__(self):
        return f'{self.MONTHS[self.date.month].main} {self.date.year}'
