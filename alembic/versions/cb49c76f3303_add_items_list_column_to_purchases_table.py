"""Add items_list column to purchases table

Revision ID: cb49c76f3303
Revises: afbee905ffb8
Create Date: 2025-06-23 13:28:33.197458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb49c76f3303'
down_revision: Union[str, Sequence[str], None] = 'afbee905ffb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchases', sa.Column('items_list', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchases', 'items_list')
    # ### end Alembic commands ###
