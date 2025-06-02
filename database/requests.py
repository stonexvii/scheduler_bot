from aiogram.types import Message

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .tables import ScheduleEvent
from datetime import datetime, date, time

import calendar


# def read_data(path: str):
#     result = []
#     with open(path, 'r', encoding='UTF-8') as file:
#         data = [line.strip().split(';;') for line in file.readlines()]
#         for entry in data:
#             year, month, day, event_time, desc = [int(item) if item.isdigit() else item for item in entry]
#             hour, minutes = map(int, event_time.split(':'))
#             event = {
#                 'date': date(year, month, day),
#                 'time': time(hour, minutes),
#                 'description': desc,
#             }
#             result.append(event)
#     return result


@connection
async def add_event(user_id: int, event_date: date, event_time: time, text: str, session: AsyncSession):
    event = ScheduleEvent(
        user_id=user_id,
        date=event_date,
        time=event_time,
        description=text,
    )
    session.add(event)
    await session.commit()



@connection
async def get_day(user_id: int, current_date: date, session: AsyncSession):
    response = await session.scalars(
        select(ScheduleEvent).where(
            ScheduleEvent.user_id == user_id,
            ScheduleEvent.date == current_date,
        ),
    )
    return response.all()


@connection
async def get_month(user_id: int, current_date: date, session: AsyncSession):
    year = current_date.year
    month = current_date.month
    first_day, last_day = 1, calendar.monthrange(year, month)[1]
    response = await session.scalars(
        select(ScheduleEvent).where(
            ScheduleEvent.user_id == user_id,
            ScheduleEvent.date.between(
                date(year, month, first_day),
                date(year, month, last_day),
            ),
        ),
    )
    return response.all()


@connection
async def delete_event(user_id: int, event_date: date, event_time: time, session: AsyncSession):
    await session.delete(delete(ScheduleEvent).where(
        ScheduleEvent.user_id == user_id,
        ScheduleEvent.date == event_date,
        ScheduleEvent.time == event_time,
    ))


#
#
# @connection
# async def get_user(message: Message, session: AsyncSession):
#     user = await session.scalar(select(Users).where(Users.id == message.from_user.id))
#     if not user:
#         user = Users(id=message.from_user.id, username=message.from_user.username)
#         session.add(user)
#         await session.commit()
#         user = await session.scalar(select(Users).where(Users.id == message.from_user.id))
#     return user
#
#
@connection
async def get_all(session: AsyncSession):
    response = await session.scalars(select(OldDatabase))
    return response.all()
#
#
# @connection
# async def user_next_question_id(user_tg_id: int, session: AsyncSession):
#     response = await session.scalars(select(UserAnswers.question_id).where(UserAnswers.user_id == user_tg_id))
#     return response.all()
#
#
# @connection
# async def add_user_answer(user_id: int, question_id: int, answer_id: int, session: AsyncSession):
#     session.add(UserAnswers(
#         user_id=user_id,
#         question_id=question_id,
#         answer_id=answer_id,
#     ))
#     await session.commit()
#
#
# @connection
# async def user_answers(user_tg_id: int, session: AsyncSession):
#     response = await session.scalars(select(UserAnswers.id).where(UserAnswers.user_id == user_tg_id))
#     return response.all()
#
#
# @connection
# async def all_users(session: AsyncSession):
#     response = await session.scalars(select(Users))
#     return response.all()
#
#
# @connection
# async def all_questions(session: AsyncSession):
#     response = await session.scalars(select(QuestionsTable))
#     return response.all()
#
#
# @connection
# async def all_answers(session: AsyncSession):
#     response = await session.scalars(select(UserAnswers))
#     return response.all()
