from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_async_session
from app.schemas import (
    GenreCreateRequestV1,
    GenreCreateResponseV1,
    GenreAlreadyExistsException,
)
from app.utils.service.genres import create_genre


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
