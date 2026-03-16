import calendar
from datetime import date, time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .tables import ScheduleEvent


@connection
async def add_event(event_date: date, event_time: time, text: str, session: AsyncSession):
    event = ScheduleEvent(
        description=text,
        date=event_date,
        time=event_time,
    )
    session.add(event)
    await session.commit()


@connection
async def get_day(current_date: date, session: AsyncSession):
    response = await session.scalars(
        select(ScheduleEvent).where(
            ScheduleEvent.date == current_date,
        ),
    )
    return response.all()


@connection
async def get_month(current_date: date, session: AsyncSession):
    year = current_date.year
    month = current_date.month
    first_day, last_day = 1, calendar.monthrange(year, month)[1]
    response = await session.scalars(
        select(ScheduleEvent).where(
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
