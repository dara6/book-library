from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.models import Genre


async def select_genre_by_name(session: AsyncSession, name: str) -> Optional[Genre]:
    stmt = select(Genre).where(Genre.name == name)
    result = await session.scalar(stmt)
    return result


async def insert_genre(session: AsyncSession, genre: Genre) -> None:
    session.add(genre)
    await session.commit()
    await session.refresh(genre)


async def select_genres(session: AsyncSession, page: int, size: int) -> list[Genre]:
    stmt = select(Genre).limit(size).offset(page * size)
    result = await session.scalars(stmt)
    return result.all()


async def select_genre_by_id(session: AsyncSession, id: int) -> Optional[Genre]:
    stmt = select(Genre).where(Genre.id == id)
    result = await session.scalar(stmt)
    return result


async def update_genre(session: AsyncSession, genre: Genre) -> None:
    await session.commit()
    await session.refresh(genre)


async def delete_genre_by_id(session: AsyncSession, id: int) -> None:
    stmt = delete(Genre).where(Genre.id == id)
    await session.execute(stmt)
    await session.commit()

