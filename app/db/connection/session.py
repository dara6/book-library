from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from app.config import get_settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_async_session_maker(self) -> sessionmaker:
        return sessionmaker(
            self.async_engine, class_=AsyncSession, expire_on_commit=False
        )

    def get_sync_session_maker(self) -> sessionmaker:
        return sessionmaker(self.sync_engine, expire_on_commit=False)

    def refresh(self) -> None:
        self.async_engine = create_async_engine(
            get_settings().database_uri_async, echo=False, future=True
        )
        self.sync_engine = create_engine(
            get_settings().database_uri_sync, echo=False, future=True
        )


async def get_async_session() -> AsyncSession:
    session_maker = SessionManager().get_async_session_maker()
    async with session_maker() as session:
        yield session


def get_sync_session() -> Session:
    session_maker = SessionManager().get_sync_session_maker()
    with session_maker() as session:
        return session


__all__ = ['get_async_session', 'get_sync_session']
