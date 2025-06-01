from aiogram import Bot, Dispatcher

import asyncio

import config
from database.requests import get_all
from database.database import create_tables
from handlers import handlers
from misc import *
from datetime import datetime


async def start_bot():
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()
    # response = await get_all()
    # with open('old_db.txt', 'w', encoding='UTF-8') as file:
    #     for line in response:
    #         file.write(';;'.join(map(str, [line.year, line.month, line.day, line.time, line.description]))+'\n')
    await create_tables()
    # await add_event(344353)
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(*handlers)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
