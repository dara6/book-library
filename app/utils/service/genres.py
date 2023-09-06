from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.genre import (
    GenreCreateOrUpdate,
    GenreAlreadyExistsException,
    GenreNotFoundException,
    GenreDetails,
    GenreBase,
    Page,
    Size,
    GenreId,
)
from app.utils.database.genres import (
    select_genre_by_name,
    insert_genre,
    select_genres,
    select_genre_by_id,
)
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


async def get_genre_details(session: AsyncSession, id: GenreId) -> GenreDetails:
    db_genre = await select_genre_by_id(session, id)
    if db_genre is None:
        raise GenreNotFoundException()
    return GenreDetails(id=db_genre.id, name=db_genre.name)
