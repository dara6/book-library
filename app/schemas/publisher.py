from pydantic import BaseModel

from typing import Optional


class PublisherId(int):
    pass


class PublisherName(str):
    pass


class PublisherAddress(str):
    pass


class PublisherWebsite(str):
    pass


class PublisherDetails(BaseModel):
    id: PublisherId
    name: PublisherName
    address: Optional[PublisherAddress]
    website: Optional[PublisherWebsite]


class PublisherCreateOrUpdate(BaseModel):
    name: PublisherName
    address: Optional[PublisherAddress]
    website: Optional[PublisherWebsite]


class PublisherCreateRequestV1(PublisherCreateOrUpdate):
    pass


class PublisherCreateResponseV1(PublisherDetails):
    pass


class PublisherNameAlreadyExistsException(BaseException):
    pass


class PublisherWebsiteAlreadyExistsException(BaseException):
    pass
