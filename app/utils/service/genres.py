from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.genre import (
    GenreCreateOrUpdate,
    GenreAlreadyExistsException,
    GenreDetails,
    GenreBase,
    Page,
    Size,
)
from app.utils.database.genres import select_genre_by_name, insert_genre, select_genres
from app.db.models import Genre


async def create_genre(
    session: AsyncSession, genre: GenreCreateOrUpdate
) -> GenreDetails:
    db_genre = await select_genre_by_name(session, genre.name)
    if db_genre is not None:
        raise GenreAlreadyExistsException()
    db_genre = Genre(name=genre.name)
    await insert_genre(session, db_genre)
    return GenreDetails(id=db_genre.id, name=db_genre.name)


async def get_genres(session: AsyncSession, page: Page, size: Size) -> list[GenreBase]:
    genres = await select_genres(session, page, size)
    return list(map(lambda genre: GenreBase(id=genre.id, name=genre.name), genres))
