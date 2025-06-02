from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from datetime import date, time

from classes.contants import MONTHS
from database.requests import add_event, get_day
from .fsm_states import AddEvent
from keyboards.keyboards import ikb_days, ikb_day_menu

command_router = Router()


@command_router.message(AddEvent.wait)
async def catch_new_event(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    current_date = data['date']
    message_data = message.text.split(' ', 1)
    if len(message_data) == 2:
        data_time = message_data[0].split(':')
        description = message_data[1]
        match data_time:
            case [hour]:
                try:
                    event_time = time(hour=int(hour))
                except:
                    event_time = None
            case [hour, minute]:
                try:
                    event_time = time(hour=int(hour), minute=int(minute))
                except:
                    event_time = None
            case _:
                event_time = None
        if event_time:
            await add_event(message.from_user.id, current_date, event_time, description)
    response = await get_day(message.from_user.id, current_date)
    message_text = f'{current_date.day} {MONTHS[current_date.month].alt} {current_date.year}\n'
    if response:
        events = '\n'.join(
            [f'{event.time.hour:0>2}:{event.time.minute:0>2} - {event.description}' for event in
             sorted(response, key=lambda x: x.time)],
        )
    else:
        events = 'В этот день нет мероприятий'
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text=message_text + events,
        reply_markup=ikb_day_menu(data['user_id'], current_date, message.from_user.id),
    )
    await state.clear()


@command_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject):
    current_date = date.today()
    user_id = int(command.args) if command.args else message.from_user.id
    await message.answer(
        text=f'{MONTHS[current_date.month].main} {current_date.year}',
        reply_markup=await ikb_days(user_id, current_date)
    )
