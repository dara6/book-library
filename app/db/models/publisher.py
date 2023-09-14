from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from app.db.models.base import BaseTable


class Publisher(BaseTable):
    __tablename__ = 'publisher'

    name = Column('name', TEXT, nullable=False, unique=True, doc='Publisher name')

    publisher_address = Column(
        'publisher_address',
        TEXT,
        doc='Publisher address',
    )

    publisher_website = Column('publisher_website', TEXT, doc='Publisher website')
