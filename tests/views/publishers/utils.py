from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.publisher import Publisher


async def get_all_publishers(session: AsyncSession) -> list[Publisher]:
    stmt = select(Publisher)
    result = await session.scalars(stmt)
    return result.all()


async def create_publisher(
    session: AsyncSession,
    name: str,
    website: Optional[str] = None,
    address: Optional[str] = None,
) -> Publisher:
    publisher = Publisher(name=name, website=website, address=address)
    session.add(publisher)
    await session.commit()
    await session.refresh(publisher)
    return publisher
