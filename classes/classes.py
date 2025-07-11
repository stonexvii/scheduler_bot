import calendar
from datetime import date

from database.requests import get_month



class EventCalendar:
    def __init__(self, current_date: date):
        self.date = current_date
        self.year = current_date.year
        self.month = current_date.month

    def days_buttons(self):
        buttons = calendar.monthcalendar(self.year, self.month)
        return buttons

    async def busy_days(self, user_id: int):
        events = await get_month(user_id, self.date)
        events = {event.date.day for event in events}
        return events
