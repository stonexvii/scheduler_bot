from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import date
from itertools import chain

from classes.classes import EventCalendar

from .callback_data import TargetDay
from database.tables import ScheduleEvent

#
# from classes.classes import Question
# from .callback_data import QuestionCB
#
#

DIGITS = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


def _int_to_str(number: int, busy_days: set[int]) -> str:
    if number:
        if number in busy_days:
            str_number = ''
            for ch in str(number):
                str_number += DIGITS[int(ch)]
            return str_number
        return str(number)
    return ' '


async def ikb_days(user_id: int, current_date: date):
    month = EventCalendar(current_date)
    buttons = month.days_buttons()
    busy_days = await month.busy_days(user_id)

    keyboard = InlineKeyboardBuilder()

    for button in chain(*buttons):
        keyboard.button(
            text=_int_to_str(button, busy_days),
            callback_data=TargetDay(
                button='td',
                year=current_date.year,
                month=current_date.month,
                day=button,
            ),
        )
        keyboard.adjust(7)
    return keyboard.as_markup()


def ikb_day_menu(events_list: list[ScheduleEvent]):
    keyboard = InlineKeyboardBuilder()
    if events_list:
        pass
    keyboard.button(
        text='Назад',
        callback_data='1',
    )
    return keyboard.as_markup()
# def ikb_answers(question: Question):
#     keyboard = InlineKeyboardBuilder()
#     # if question.id:
#     for answer in question:
#         keyboard.button(
#             text=answer.text,
#             callback_data=QuestionCB(
#                 button='user_choice',
#                 question_id=question.id,
#                 answer_id=answer.id,
#             ),
#         )
#     # else:
#     #     keyboard.button(
#     #         text='Начать',
#     #         callback_data=QuestionCB(
#     #             button='user_choice',
#     #             question_id=0,
#     #             answer_id=0,
#     #         ),
#     #     )
#     keyboard.adjust(1)
#     return keyboard.as_markup()
