import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.views.publishers import create_publisher, get_all_publishers


ENDPOINT = '/v1/publishers'


@pytest.mark.parametrize(
    'body',
    [
        {'name': 'publisher'},
        {
            'name': 'издательство',
            'website': 'isdatelstvo.ru',
            'address': 'ул Энтузиастов, д.9, кв. 5',
        },
    ],
)
async def test_success_create(session: AsyncSession, client: AsyncClient, body: dict):
    response = await client.post(ENDPOINT, json=body)

    assert response.status_code == 200
    assert response.json()['name'] == body['name']


async def test_name_already_exist(session: AsyncSession, client: AsyncClient):
    name = 'издательство'
    await create_publisher(session, name)

    body = {'name': name}
    response = await client.post(ENDPOINT, json=body)

    assert response.status_code == 409

    publishers = await get_all_publishers(session)
    assert len(publishers) == 1


async def test_website_already_exists(session: AsyncSession, client: AsyncClient):
    name_1 = 'puk'
    name_2 = 'pukipuk'
    website = 'puk.ru'
    await create_publisher(session, name_1, website)

    body = {'name': name_2, 'website': website}
    response = await client.post(ENDPOINT, json=body)

    assert response.status_code == 409

    publishers = await get_all_publishers(session)
    assert len(publishers) == 1
