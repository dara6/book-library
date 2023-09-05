from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Genre


async def get_all_genres(session: AsyncSession) -> list[Genre]:
    stmt = select(Genre)
    result = await session.scalars(stmt)
    return result.all()


async def create_genre(session: AsyncSession, name: str) -> Genre:
    genre = Genre(name=name)
    session.add(genre)
    await session.commit()
    await session.refresh(genre)
    return genre
