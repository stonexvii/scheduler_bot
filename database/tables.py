from datetime import date, time

from sqlalchemy import String, BigInteger, Integer, Date, Time, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class ScheduleEvent(Base):
    __tablename__ = 'schedule_events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[date] = mapped_column(Date)
    time: Mapped[time] = mapped_column(Time(timezone=False))
    description: Mapped[str] = mapped_column(String(700), nullable=False)
    public: Mapped[bool] = mapped_column(Boolean, default=False)
