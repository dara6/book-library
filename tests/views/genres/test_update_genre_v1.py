import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.views.genres import create_genre, get_all_genres

ENDPOINT = '/v1/genres/{genre_id}'


@pytest.mark.parametrize('old_name, new_name', [('myau', 'myaaau'), ('myau', 'myau')])
async def test_success_update(
    client: AsyncClient, session: AsyncSession, old_name: str, new_name: str
):
    db_genre = await create_genre(session, old_name)
    body = {'name': new_name}
    expected_genre = {'id': db_genre.id, 'name': new_name}

    response = await client.put(get_endpoint(db_genre.id), json=body)
    assert response.status_code == 200
    assert response.json() == expected_genre

    genres = await get_all_genres(session)
    assert genres == [db_genre]


async def test_not_found(client: AsyncClient, session: AsyncSession):
    id_not_in_db = 1000

    body = {'name': 'aaaaa'}
    response = await client.put(get_endpoint(id_not_in_db), json=body)

    assert response.status_code == 404

    assert await get_all_genres(session) == []


async def test_already_exists(client: AsyncClient, session: AsyncSession):
    name_1 = 'puk'
    name_2 = 'puuk'

    genre_1 = await create_genre(session, name_1)
    genre_2 = await create_genre(session, name_2)

    body = {'name': name_2}
    response = await client.put(get_endpoint(genre_1.id), json=body)

    assert response.status_code == 409

    genres = await get_all_genres(session)
    assert genres == [genre_1, genre_2]


def get_endpoint(genre_id: int) -> str:
    return ENDPOINT.format(genre_id=genre_id)
