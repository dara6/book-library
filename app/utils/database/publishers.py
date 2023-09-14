from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Publisher


async def select_publisher_by_name(
    session: AsyncSession, name: str
) -> Optional[Publisher]:
    stmt = select(Publisher).where(Publisher.name == name)
    result = await session.scalar(stmt)
    return result


async def insert_publisher(session: AsyncSession, publisher: Publisher) -> None:
    session.add(publisher)
    await session.commit()
    await session.refresh(publisher)
