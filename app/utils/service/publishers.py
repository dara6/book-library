from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.publisher import (
    PublisherDetails,
    PublisherAlreadyExistsException,
    PublisherCreateOrUpdate,
)

from app.utils.database.publishers import select_publisher_by_name, insert_publisher
from app.db.models import Publisher


async def create_publisher(
    session: AsyncSession, publisher: PublisherCreateOrUpdate
) -> PublisherDetails:
    db_publisher = await select_publisher_by_name(session, publisher.name)
    if db_publisher is not None:
        raise PublisherAlreadyExistsException()
    db_publisher = Publisher(
        name=publisher.name,
        publisher_address=publisher.address,
        publisher_website=publisher.website,
    )
    await insert_publisher(session, db_publisher)
    return PublisherDetails(
        id=db_publisher.id,
        name=db_publisher.name,
        address=db_publisher.publisher_address,
        website=db_publisher.publisher_address,
    )
