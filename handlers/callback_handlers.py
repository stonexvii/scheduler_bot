from datetime import date

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from classes import EventCalendar
from database.requests import get_day, delete_event
from keyboards.callback_data import TargetDay
from keyboards.keyboards import ikb_days, ikb_day_menu, ikb_select_month, ikb_delete_events
from misc import time_formater
from .fsm_states import AddEvent

callback_router = Router()


@callback_router.callback_query(TargetDay.filter(F.button == 'main'))
async def main_menu(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    current_date = date(callback_data.year, callback_data.month, callback_data.day)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'{EventCalendar.MONTHS[current_date.month].main} {current_date.year}',
        reply_markup=await ikb_days(callback_data.user_id, current_date),
    )


@callback_router.callback_query(TargetDay.filter(F.button == 'td'))
async def target_day_handler(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    day, month, year = callback_data.day, callback_data.month, callback_data.year
    inline_message = 'Нет такого дня'
    if day:
        inline_message = f'{day} {EventCalendar.MONTHS[month].alt} {year}'
        current_date = date(year, month, day)
        response = await get_day(callback_data.user_id, current_date)
        message_text = f'{inline_message}\n'
        if response:
            events = '\n'.join(
                [f'{time_formater(event.time)} - {event.description}' for event in
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
    await callback.answer(
        text=inline_message,
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
    )


@callback_router.callback_query(TargetDay.filter(F.button == 'de'))
async def select_delete_event(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    day, month, year = callback_data.day, callback_data.month, callback_data.year
    current_date = date(year, month, day)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Какое мероприятие хотите удалить?:',
        reply_markup=await ikb_delete_events(callback_data.user_id, current_date),
    )


@callback_router.callback_query(TargetDay.filter(F.button == 'ed'))
async def delete_event_handler(callback: CallbackQuery, callback_data: TargetDay, bot: Bot):
    await delete_event(callback_data.option)
    await target_day_handler(callback, callback_data, bot)
    await callback.answer(
        text='Событие удалено!',
        show_alert=True,
    )
