from datetime import date, timedelta
from itertools import chain

from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.classes import EventCalendar
from database.requests import get_day
from misc import time_formater
from .buttons import TargetDayButton
from .callback_data import TargetDay


def _int_to_str(number: int, busy_days: set[int]) -> str:
    digits = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    if number:
        if number in busy_days:
            str_number = ''
            for ch in str(number):
                str_number += digits[int(ch)]
            return str_number
        return str(number)
    return ' '


async def ikb_days(user_id: int, current_date: date):
    month = EventCalendar(current_date)
    buttons = month.days_buttons()
    busy_days = await month.busy_days(user_id)
    prev_month, next_month = month.prev_next()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        **TargetDayButton(
            text=f'<<< {EventCalendar.MONTHS[prev_month.month].main}',
            button='main',
            user_tg_id=user_id,
            date=prev_month,
        ).as_kwargs(),
    )
    keyboard.button(
        **TargetDayButton(
            text=str(month),
            button='sm',
            user_tg_id=user_id,
            date=current_date,
            day=1,
        ).as_kwargs(),
    )
    keyboard.button(
        **TargetDayButton(
            text=f'{EventCalendar.MONTHS[next_month.month].main} >>>',
            button='main',
            user_tg_id=user_id,
            date=next_month,
            day=1,
        ).as_kwargs(),
    )
    for button in chain(*buttons):
        keyboard.button(
            **TargetDayButton(
                text=_int_to_str(button, busy_days),
                button='td',
                user_tg_id=user_id,
                date=current_date,
                day=button,
            ).as_kwargs(),
        )
        keyboard.adjust(3, 7)
    return keyboard.as_markup()


def ikb_day_menu(user_id: int, current_date: date, admin_id: int):
    keyboard = InlineKeyboardBuilder()
    prev_day = current_date - timedelta(days=1)
    next_day = current_date + timedelta(days=1)
    keyboard_adjust = (2, 1)
    keyboard.button(
        **TargetDayButton(
            text='<<<',
            button='td',
            user_tg_id=user_id,
            date=prev_day,
        ).as_kwargs(),
    )
    keyboard.button(
        **TargetDayButton(
            text='>>>',
            button='td',
            user_tg_id=user_id,
            date=next_day,
        ).as_kwargs(),
    )
    if user_id == admin_id:
        keyboard.button(
            **TargetDayButton(
                text='Добавить',
                button='ae',
                user_tg_id=admin_id,
                date=current_date,
            ).as_kwargs(),
        )
        keyboard.button(
            **TargetDayButton(
                text='Удалить',
                button='de',
                user_tg_id=admin_id,
                date=current_date,
            ).as_kwargs(),
        )
        keyboard_adjust = (2, 2, 1)
    keyboard.button(
        **TargetDayButton(
            text='Назад',
            button='main',
            user_tg_id=admin_id,
            date=current_date,
        ).as_kwargs(),
    )
    keyboard.adjust(*keyboard_adjust)
    return keyboard.as_markup()


def ikb_select_month(user_id: int, current_date: date):
    keyboard = InlineKeyboardBuilder()
    for idx, month in enumerate(EventCalendar.MONTHS):
        if idx:
            keyboard.button(
                text=month.main,
                callback_data=TargetDay(
                    button='main',
                    user_id=user_id,
                    year=current_date.year,
                    month=idx,
                    day=1,
                )
            )
    keyboard.adjust(3)
    return keyboard.as_markup()


async def ikb_delete_events(user_id: int, events_date: date):
    events = await get_day(user_id, events_date)
    keyboard = InlineKeyboardBuilder()
    for event in sorted(events, key=lambda x: x.time):
        keyboard.button(
            text=f'❌ {time_formater(event.time)} - {event.description}',
            callback_data=TargetDay(
                button='ed',
                user_id=user_id,
                year=events_date.year,
                month=events_date.month,
                day=events_date.day,
                option=event.id,
            )
        )
    keyboard.button(
        **TargetDayButton(
            text=f'Назад',
            button='td',
            user_tg_id=user_id,
            date=events_date,
        ).as_kwargs(),
    )
    keyboard.adjust(1),
    return keyboard.as_markup()
