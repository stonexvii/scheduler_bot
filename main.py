import asyncio

from aiogram import Bot, Dispatcher

import config
from database.database import create_tables
from handlers import handlers
from misc import *


async def start_bot():
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()
    await create_tables()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(*handlers)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
