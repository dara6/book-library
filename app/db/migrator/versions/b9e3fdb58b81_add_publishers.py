"""add publishers

Revision ID: b9e3fdb58b81
Revises: 4a3d41e94684
Create Date: 2023-09-14 18:43:19.954810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9e3fdb58b81'
down_revision: Union[str, None] = '4a3d41e94684'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'publishers',
        sa.Column('name', sa.TEXT(), nullable=False),
        sa.Column('address', sa.TEXT(), nullable=True),
        sa.Column('website', sa.TEXT(), nullable=True),
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
        sa.PrimaryKeyConstraint('id', name=op.f('pk__publishers')),
        sa.UniqueConstraint('name', name=op.f('uq__publishers__name')),
        sa.UniqueConstraint('website', name=op.f('uq__publishers__website')),
    )


def downgrade() -> None:
    op.drop_table('publishers')
