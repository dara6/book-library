from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_async_session
from app.schemas import (
    PublisherCreateRequestV1,
    PublisherCreateResponseV1,
    PublisherNameAlreadyExistsException,
    PublisherWebsiteAlreadyExistsException,
)
from app.utils.service.publishers import create_publisher


api_router_v1 = APIRouter(prefix='/v1', tags=['publishers'])


@api_router_v1.post(
    '/publishers',
    responses={
        status.HTTP_409_CONFLICT: {
            'description': 'Publisher name or website is already exists'
        }
    },
)
async def create_publisher_v1_views(
    body: PublisherCreateRequestV1, session: AsyncSession = Depends(get_async_session)
) -> PublisherCreateResponseV1:
    try:
        publisher = await create_publisher(session, body)
        return publisher
    except PublisherNameAlreadyExistsException:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail='Publisher name is already exists'
        )
    except PublisherWebsiteAlreadyExistsException:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail='Publisher website is already exists'
        )
