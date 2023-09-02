from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get('ENV', 'local')

    APP_HOST: str = environ.get('APP_HOST', 'http://127.0.0.1')
    APP_PORT: int = int(environ.get('APP_PORT', 8000))

    POSTGRES_DB: str = environ.get('POSTGRES_DB', 'book_library')
    POSTGRES_USER: str = environ.get('POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD: str = environ.get('POSTGRES_PASSWORD', 'admin')
    POSTGRES_HOST: str = environ.get('POSTGRES_HOST', 'db')
    POSTGRES_PORT: int = int(environ.get('POSTGRES_INTERNAL_PORT', 5432))

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            'database': self.POSTGRES_DB,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT,
        }

    @property
    def database_uri_async(self) -> str:
        """
        Get uri for connection with database.
        """
        return 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'.format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            **self.database_settings,
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
