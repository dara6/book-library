from os import environ
from types import SimpleNamespace
from uuid import uuid4

from asyncio import get_event_loop_policy
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from alembic.command import upgrade
from alembic.config import Config

from app.main import get_application
from app.config import get_settings
from app.db.connection import SessionManager
from tests.utils import make_alembic_config


pytest_plugins = ['pytest_asyncio']


def run_upgrade(connection, cfg):
    cfg.attributes['connection'] = connection
    upgrade(cfg, 'head')


async def run_async_upgrade(config: Config, database_uri: str):
    async_engine = create_async_engine(database_uri, echo=False)
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, config)


@pytest.fixture(scope='session')
def event_loop():
    """
    Creates event loop for tests.
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """
    settings = get_settings()

    tmp_name = '.'.join([uuid4().hex, 'pytest'])
    settings.POSTGRES_DB = tmp_name
    environ['POSTGRES_DB'] = tmp_name

    tmp_url = settings.database_uri_sync
    if not database_exists(tmp_url):
        create_database(tmp_url)

    try:
        yield settings.database_uri_async
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(
        config='./', name='alembic', pg_url=postgres, raiseerr=False, x=None
    )
    return make_alembic_config(cmd_options)


@pytest.fixture
async def migrated_postgres(postgres, alembic_config: Config):
    """
    Проводит миграции.
    """
    await run_async_upgrade(alembic_config, postgres)
    return postgres


@pytest.fixture
async def engine_async(migrated_postgres) -> AsyncEngine:
    engine = create_async_engine(migrated_postgres, future=True)
    yield engine
    await engine.dispose()


@pytest.fixture
def session_factory_async(engine_async) -> sessionmaker:
    return sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def session(session_factory_async) -> AsyncSession:
    async with session_factory_async() as session:
        yield session


@pytest.fixture
async def client(
    migrated_postgres, manager: SessionManager = SessionManager()
) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_application()
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    yield AsyncClient(app=app, base_url='http://test')
