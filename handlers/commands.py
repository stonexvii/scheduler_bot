from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import MessageEntityType

from database.requests import get_month
# from classes.classes import Question, User
# from database.requests import all_questions, all_answers, add_new_question, all_users, user_answers
# from keyboards.keyboards import ikb_answers
from .fsm_states import NewQuestion, StartTest
from e_sender.email_sender import send_mail

from datetime import date, time

from classes.classes import EventCalendar
from database.requests import add_event
from keyboards.keyboards import ikb_days

import config

command_router = Router()


@command_router.message(Command('load'))
async def command_load_db(message: Message):
    await add_event(message.from_user.id)


@command_router.message(Command('start'))
async def command_start(message: Message):
    current_date = date.today()
    await message.answer(
        text='Календарь на месяц',
        reply_markup=await ikb_days(message.from_user.id, current_date)
    )
    # response = await get_month(message.from_user.id, current_date)
    # for entry in response:
    #     print(entry.date_time, entry.description)
    # await bot.delete_message(
    #     chat_id=message.from_user.id,
    #     message_id=message.message_id,
    # )
    # user = await User.from_db(message)
    # next_question_id = await user.next_question_id
    # question = await Question.from_db(next_question_id)
    # if question:
    #     await state.set_state(StartTest.wait_question)
    #     keyboard = ikb_answers(question=question)
    #     if question.video_id:
    #         await bot.send_video(
    #             chat_id=message.from_user.id,
    #             video=question.video_id,
    #             caption=question.text,
    #             reply_markup=keyboard,
    #         )
    #     else:
    #         await bot.send_message(
    #             chat_id=message.from_user.id,
    #             text=question.text,
    #             reply_markup=keyboard,
    #         )
#
#
# @command_router.message(Command('add'))
# async def command_add(message: Message, state: FSMContext):
#     await message.answer(
#         text='Пришли вопрос и ответы'
#     )
#     await state.set_state(NewQuestion.question_catch)
#
#
# @command_router.message(NewQuestion.question_catch)
# async def new_question(message: Message, state: FSMContext):
#     msg = message.caption if message.video else message.text
#     if not (msg.startswith('0') or msg.startswith('100')):
#         question_id, question, *answers = msg.split('\n')
#         video_id = message.video.file_id if message.video else None
#     else:
#         question_id, question, *answers = msg.split('\n', 1)
#         video_id = message.video.file_id if message.video else None
#     await add_new_question(int(question_id), question, answers, video_id)
#     await state.clear()
