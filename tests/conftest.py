from fastapi.testclient import TestClient
import pytest

from app.main import app


pytest_plugins = ['pytest_asyncio']


@pytest.fixture
async def client():
    yield TestClient(app)
