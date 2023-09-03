from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.genre import (
    GenreCreateOrUpdate,
    GenreAlreadyExistsException,
    GenreDetails,
)
from app.utils.database.genres import get_genre_by_name, insert_genre
from app.db.models import Genre


async def create_genre(
    session: AsyncSession, genre: GenreCreateOrUpdate
) -> GenreDetails:
    db_genre = await get_genre_by_name(session, genre.name)
    if db_genre is not None:
        raise GenreAlreadyExistsException()
    db_genre = Genre(name=genre.name)
    await insert_genre(session, db_genre)
    return GenreDetails(id=db_genre.id, name=db_genre.name)
