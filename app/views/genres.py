from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_async_session
from app.schemas import (
    Page,
    Size,
    GenreCreateRequestV1,
    GenreCreateResponseV1,
    GenreAlreadyExistsException,
    GenreGetListResponseV1,
)
from app.utils.service.genres import create_genre, get_genres


api_router_v1 = APIRouter(
    prefix='/v1',
    tags=['genres'],
)


@api_router_v1.post(
    '/genres',
    responses={status.HTTP_409_CONFLICT: {'description': 'Genre name already exists'}},
)
async def create_genre_v1_views(
    body: GenreCreateRequestV1, session: AsyncSession = Depends(get_async_session)
) -> GenreCreateResponseV1:
    try:
        genre = await create_genre(session, body)
        return genre
    except GenreAlreadyExistsException:
        raise HTTPException(status.HTTP_409_CONFLICT)


@api_router_v1.get('/genres')
async def get_list_of_genres_v1_views(
    page: Page = Query(default=0, ge=0),
    size: Size = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
) -> GenreGetListResponseV1:
    genres = await get_genres(session, page, size)
    return GenreGetListResponseV1(genres=genres, page=page, size=size)
