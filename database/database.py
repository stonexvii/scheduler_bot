from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB
from .tables import Base

engine = create_async_engine(
    url=f'postgresql+asyncpg://{DB.user}:{DB.password}@{DB.host}:{DB.port}/{DB.name}',
    echo=False,
)

async_session = async_sessionmaker(engine)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


def connection(function):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await function(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
