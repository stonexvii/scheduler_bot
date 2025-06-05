from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import date, time, timedelta
from itertools import chain

from classes.classes import EventCalendar
from classes.contants import MONTHS, DIGITS
from .callback_data import TargetDay
from database.requests import get_day
from misc import time_formater


def _int_to_str(number: int, busy_days: set[int]) -> str:
    if number:
        if number in busy_days:
            str_number = ''
            for ch in str(number):
                str_number += DIGITS[int(ch)]
            return str_number
        return str(number)
    return ' '


def _prev_month(current_date: date) -> date:
    if current_date.month == 1:
        month = 12
        year = current_date.year - 1
    else:
        month = current_date.month - 1
        year = current_date.year
    return current_date.replace(year=year, month=month)


def _next_month(current_date: date):
    if current_date.month == 12:
        month = 1
        year = current_date.year + 1
    else:
        month = current_date.month + 1
        year = current_date.year
    return current_date.replace(year=year, month=month)


async def ikb_days(user_id: int, current_date: date):
    month = EventCalendar(current_date)
    _prev_month(current_date)
    buttons = month.days_buttons()
    busy_days = await month.busy_days(user_id)
    prev_month = _prev_month(current_date)
    next_month = _next_month(current_date)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=f'<<< {MONTHS[prev_month.month].main}',
        callback_data=TargetDay(
            button='main',
            user_id=user_id,
            year=prev_month.year,
            month=prev_month.month,
            day=1,
        )
    )
    keyboard.button(
        text=f'{MONTHS[current_date.month].main} {current_date.year}',
        callback_data=TargetDay(
            button='sm',
            user_id=user_id,
            year=current_date.year,
            month=current_date.month,
            day=1,
        )
    )
    keyboard.button(
        text=f'{MONTHS[next_month.month].main} >>>',
        callback_data=TargetDay(
            button='main',
            user_id=user_id,
            year=next_month.year,
            month=next_month.month,
            day=1,
        )
    )
    for button in chain(*buttons):
        keyboard.button(
            text=_int_to_str(button, busy_days),
            callback_data=TargetDay(
                button='td',
                user_id=user_id,
                year=current_date.year,
                month=current_date.month,
                day=button,
            ),
        )
        keyboard.adjust(3, 7)
    return keyboard.as_markup()


def ikb_day_menu(user_id: int, current_date: date, admin_id: int):
    keyboard = InlineKeyboardBuilder()
    prev_day = current_date - timedelta(days=1)
    next_day = current_date + timedelta(days=1)
    keyboard_adjust = (2, 1)
    keyboard.button(
        text='<<<',
        callback_data=TargetDay(
            button='td',
            user_id=user_id,
            year=prev_day.year,
            month=prev_day.month,
            day=prev_day.day,
        ),
    )
    keyboard.button(
        text='>>>',
        callback_data=TargetDay(
            button='td',
            user_id=user_id,
            year=next_day.year,
            month=next_day.month,
            day=next_day.day,
        ),
    )
    if user_id == admin_id:
        keyboard.button(
            text='Добавить',
            callback_data=TargetDay(
                button='ae',
                user_id=admin_id,
                year=current_date.year,
                month=current_date.month,
                day=current_date.day,
            ),
        )
        keyboard.button(
            text='Удалить',
            callback_data=TargetDay(
                button='de',
                user_id=admin_id,
                year=current_date.year,
                month=current_date.month,
                day=current_date.day,
            ),
        )
        keyboard_adjust = (2, 2, 1)
    keyboard.button(
        text='Назад',
        callback_data=TargetDay(
            button='main',
            user_id=user_id,
            year=current_date.year,
            month=current_date.month,
            day=current_date.day,
        ),
    )
    keyboard.adjust(*keyboard_adjust)
    return keyboard.as_markup()


def ikb_select_month(user_id: int, current_date: date):
    keyboard = InlineKeyboardBuilder()
    for idx, month in enumerate(MONTHS):
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
        text='Назад',
        callback_data=TargetDay(
            button='td',
            user_id=user_id,
            year=events_date.year,
            month=events_date.month,
            day=events_date.day,
        )
    )
    keyboard.adjust(1),
    return keyboard.as_markup()
