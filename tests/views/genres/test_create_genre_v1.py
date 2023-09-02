import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Genre

ENDPOINT = '/v1/genres'


@pytest.mark.parametrize('name', ['puk', 'пук'])
async def test_success_create(client: AsyncClient, session: AsyncSession, name: str):
    body = {'name': name}
    response = await client.post(ENDPOINT, json=body)
    assert response.status_code == 200
    assert response.json()['name'] == body['name']
    genres = await get_all_genres(session)
    assert len(genres) == 1
    assert genres[0].name == body['name']


async def test_already_exists(client: AsyncClient, session: AsyncSession):
    await create_genre(session, 'puk')
    body = {'name': 'puk'}
    response = await client.post(ENDPOINT, json=body)
    assert response.status_code == 409
    genres = await get_all_genres(session)
    assert len(genres) == 1


async def get_all_genres(session: AsyncSession):
    stmt = select(Genre)
    result = await session.scalars(stmt)
    return result.all()


async def create_genre(session: AsyncSession, name: str):
    genre = Genre(name=name)
    session.add(genre)
    await session.commit()
    await session.refresh(genre)
    return genre
