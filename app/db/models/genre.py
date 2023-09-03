from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from .base import BaseTable


class Genre(BaseTable):
    __tablename__ = 'genres'

    name = Column('name', TEXT, nullable=False, unique=True, doc='Genre name')
