import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.views.publishers import create_publisher, get_all_publishers


ENDPOINT = '/v1/publishers'


@pytest.mark.parametrize('name', ['publisher', 'издательство'])
async def test_success_create(session: AsyncSession, client: AsyncClient, name: str):
    body = {'name': name}
    response = await client.post(ENDPOINT, json=body)

    assert response.status_code == 200
    assert response.json()['name'] == body['name']


async def test_alredy_exist(session: AsyncSession, client: AsyncClient):
    await create_publisher(session, 'издательство')

    body = {'name': 'издательство'}
    response = await client.post(ENDPOINT, json=body)

    assert response.status_code == 409

    publishers = await get_all_publishers(session)
    assert len(publishers) == 1
