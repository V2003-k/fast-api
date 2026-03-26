"""add content column to post table

Revision ID: 58b58fd94a43
Revises: 2a18d33a61f6
Create Date: 2025-11-20 23:48:33.960887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58b58fd94a43'
down_revision: Union[str, Sequence[str], None] = '2a18d33a61f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
