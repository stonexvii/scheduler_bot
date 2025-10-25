import os
from collections import namedtuple

import dotenv

DataBase = namedtuple('DataBase', ['password', 'user', 'name', 'host', 'port'])
dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB = DataBase(
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_USER'),
    os.getenv('DB_NAME'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
)
