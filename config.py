import dotenv
import os

# dotenv.load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')