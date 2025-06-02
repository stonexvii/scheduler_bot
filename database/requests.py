from aiogram.types import Message

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .tables import ScheduleEvent
from datetime import date, time

import calendar


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
async def delete_event(event_id: int, session: AsyncSession):
    event = await session.scalar(
        select(ScheduleEvent).where(
            ScheduleEvent.id == event_id,
        ),
    )
    await session.delete(event)
    await session.commit()
