from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from app.db.models.base import BaseTable


class Publisher(BaseTable):
    __tablename__ = 'publishers'

    name = Column('name', TEXT, nullable=False, unique=True, doc='Publisher name')

    address = Column(
        'address',
        TEXT,
        doc='Publisher address',
    )

    website = Column('website', TEXT, unique=True, doc='Publisher website')
