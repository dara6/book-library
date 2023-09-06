from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.views.genres import create_genre

ENDPOINT = '/v1/genres/{genre_id}'


async def test_success(session: AsyncSession, client: AsyncClient):
    db_genre = await create_genre(session, 'myau')
    expected_genre = {'id': db_genre.id, 'name': db_genre.name}

    response = await client.get(get_endpoint(db_genre.id))
    assert response.status_code == 200
    assert response.json() == expected_genre


async def test_not_found(client: AsyncClient):
    id_not_in_db = 1000
    response = await client.get(get_endpoint(id_not_in_db))
    assert response.status_code == 404


def get_endpoint(genre_id: int) -> str:
    return ENDPOINT.format(genre_id=genre_id)
