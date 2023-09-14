from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.publisher import (
    PublisherDetails,
    PublisherNameAlreadyExistsException,
    PublisherWebsiteAlreadyExistsException,
    PublisherCreateOrUpdate,
)

from app.utils.database.publishers import (
    select_publisher_by_name,
    select_publisher_by_website,
    insert_publisher,
)
from app.db.models import Publisher


async def create_publisher(
    session: AsyncSession, publisher: PublisherCreateOrUpdate
) -> PublisherDetails:
    db_publisher = await select_publisher_by_name(session, publisher.name)
    if db_publisher is not None:
        raise PublisherNameAlreadyExistsException()

    if publisher.website is not None:
        db_publisher = await select_publisher_by_website(session, publisher.website)
        if db_publisher is not None:
            raise PublisherWebsiteAlreadyExistsException()

    db_publisher = Publisher(
        name=publisher.name,
        address=publisher.address,
        website=publisher.website,
    )
    await insert_publisher(session, db_publisher)
    return PublisherDetails(
        id=db_publisher.id,
        name=db_publisher.name,
        address=db_publisher.address,
        website=db_publisher.address,
    )
