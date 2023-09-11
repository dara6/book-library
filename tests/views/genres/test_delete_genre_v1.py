from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.views.genres import create_genre, get_all_genres

ENDPOINT = '/v1/genres/{genre_id}'


async def test_success_delete(session: AsyncSession, client: AsyncClient):
    name = 'bukashka'
    genre = await create_genre(session, name)
    response = await client.delete(get_endpoint(genre.id))
    assert response.status_code == 200
    assert await get_all_genres(session) == []


async def test_not_found(client: AsyncClient):
    id_not_in_db = 1000
    response = await client.delete(get_endpoint(id_not_in_db))
    assert response.status_code == 404


def get_endpoint(genre_id: int) -> str:
    return ENDPOINT.format(genre_id=genre_id)
