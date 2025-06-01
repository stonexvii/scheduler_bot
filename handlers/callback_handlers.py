from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

# from classes.classes import Question
# from database.requests import add_user_answer
# from keyboards.keyboards import ikb_answers
# from keyboards.callback_data import QuestionCB
# from .fsm_states import StartTest

from datetime import date, time

from classes.contants import MONTHS
from database.requests import get_day
from keyboards.callback_data import TargetDay

callback_router = Router()


@callback_router.callback_query(TargetDay.filter(F.button == 'td'))
async def target_day_handler(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    await callback.answer(
        text=f'{callback_data.year} {callback_data.month} {callback_data.day}',
        show_alert=True,
    )
    day, month, year = callback_data.day, callback_data.month, callback_data.year
    current_date = date(year, month, day)
    response = await get_day(callback.from_user.id, current_date)
    message_text = f'{day} {MONTHS[month]} {year}\n'
    if response:
        events = '\n'.join(
            [f'{event.time.hour:0>2}:{event.time.minute:0>2} - {event.description}' for event in response],
        )
    else:
        events = 'В этот день нет мероприятий'
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_text + events,
    )
