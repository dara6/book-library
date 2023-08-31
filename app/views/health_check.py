from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from starlette import status

from app.db.connection import get_async_session
from app.schemas import PingResponse


api_router = APIRouter(
    prefix='/health_check',
    tags=['Application Health'],
)


@api_router.get(
    '/ping_application',
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def ping_application():
    return PingResponse()


@api_router.get(
    '/ping_database',
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def ping_database(
    session: AsyncSession = Depends(get_async_session),
):
    await session.execute(select(text('1')))
    return PingResponse()
