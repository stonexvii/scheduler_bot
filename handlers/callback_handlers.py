from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import date, time

from classes.contants import MONTHS
from database.requests import get_day
from .fsm_states import AddEvent
from keyboards.keyboards import ikb_days, ikb_day_menu, ikb_select_month
from keyboards.callback_data import TargetDay

callback_router = Router()


@callback_router.callback_query(TargetDay.filter(F.button == 'main'))
async def main_menu(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    current_date = date(callback_data.year, callback_data.month, callback_data.day)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'{MONTHS[current_date.month].main} {current_date.year}',
        reply_markup=await ikb_days(callback_data.user_id, current_date),
    )


@callback_router.callback_query(TargetDay.filter(F.button == 'td'))
async def target_day_handler(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    await callback.answer(
        text=f'{callback_data.year} {callback_data.month} {callback_data.day}',
    )
    day, month, year = callback_data.day, callback_data.month, callback_data.year
    current_date = date(year, month, day)
    response = await get_day(callback.from_user.id, current_date)
    message_text = f'{day} {MONTHS[month].alt} {year}\n'
    if response:
        events = '\n'.join(
            [f'{event.time.hour:0>2}:{event.time.minute:0>2} - {event.description}' for event in
             sorted(response, key=lambda x: x.time)],
        )
    else:
        events = 'В этот день нет мероприятий'
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_text + events,
        reply_markup=ikb_day_menu(callback_data.user_id, current_date, callback.from_user.id),
    )


@callback_router.callback_query(TargetDay.filter(F.button == 'sm'))
async def select_month(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    await callback.answer(
        text=f'{callback_data.year} {callback_data.month} {callback_data.day}',
    )
    day, month, year = callback_data.day, callback_data.month, callback_data.year
    current_date = date(year, month, day)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Выберите месяц:',
        reply_markup=ikb_select_month(callback_data.user_id, current_date),
    )


@callback_router.callback_query(TargetDay.filter(F.button == 'ae'))
async def add_event(callback: CallbackQuery, callback_data: TargetDay, bot: Bot, state: FSMContext):
    await state.set_state(AddEvent.wait)
    await callback.answer(
        text=f'{callback_data.year} {callback_data.month} {callback_data.day}',
    )
    day, month, year = callback_data.day, callback_data.month, callback_data.year
    current_date = date(year, month, day)
    data = {
        'user_id': callback_data.user_id,
        'date': current_date,
        'chat_id': callback.from_user.id,
        'message_id': callback.message.message_id,
    }
    await state.update_data(data)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Введите время и описание мероприятия:',
        # reply_markup=ikb_select_month(callback_data.user_id, current_date),
    )

# @callback_router.callback_query(TargetDay.filter(F.button == 'de'))
# async def delete_event(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
#     await callback.answer(
#         text=f'{callback_data.year} {callback_data.month} {callback_data.day}',
#     )
#     day, month, year = callback_data.day, callback_data.month, callback_data.year
#     current_date = date(year, month, day)
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text='Выберите месяц:',
#         reply_markup=ikb_select_month(callback_data.user_id, current_date),
#     )
