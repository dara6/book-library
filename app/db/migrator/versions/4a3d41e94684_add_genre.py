"""add genre

Revision ID: 4a3d41e94684
Revises: 
Create Date: 2023-09-01 18:02:50.304621

"""  # noqa: W291
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4a3d41e94684'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'genres',
        sa.Column('name', sa.TEXT(), nullable=False),
        sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column(
            'dt_created',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'dt_updated',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__genres')),
        sa.UniqueConstraint('name', name=op.f('uq__genres__name')),
    )


def downgrade() -> None:
    op.drop_table('genres')
