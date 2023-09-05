import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Genre
from tests.views.genres import create_genre

ENDPOINT = '/v1/genres'


@pytest.mark.parametrize('count', [0, 2])
async def test_list_of_genres(client: AsyncClient, session: AsyncSession, count: int):
    db_genres = [await create_genre(session, str(i)) for i in range(count)]
    expected_genres = list(map(db_genre_to_dict, db_genres))

    response = await client.get(ENDPOINT)
    assert response.status_code == 200
    assert response.json()['genres'] == expected_genres


@pytest.mark.parametrize(
    'page, size, expected_count',
    [(0, 1, 1), (0, 5, 5), (0, 10, 10), (1, 7, 3), (1, 10, 0)],
)
async def test_pagination(
    client: AsyncClient,
    session: AsyncSession,
    page: int,
    size: int,
    expected_count: int,
):
    count = 10
    for i in range(count):
        await create_genre(session, str(i))

    response = await client.get(ENDPOINT, params={'page': page, 'size': size})
    assert response.json()['page'] == page
    assert response.json()['size'] == size
    assert len(response.json()['genres']) == expected_count


def db_genre_to_dict(db_genre: Genre):
    return {'id': db_genre.id, 'name': db_genre.name}
