import config


class DBSettings:
    DB_USER = config.DB_USER
    DB_PASSWORD = config.DB_PASSWORD
    DB_HOST = config.DB_HOST
    DB_PORT = config.DP_PORT
    DB_NAME = config.DB_NAME

    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
