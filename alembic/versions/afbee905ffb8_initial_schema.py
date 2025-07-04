"""initial schema

Revision ID: afbee905ffb8
Revises: 
Create Date: 2025-06-22 17:11:03.363700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'afbee905ffb8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('branches',
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_branches_id'), 'branches', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('unit_price', sa.NUMERIC(), nullable=False),
    sa.CheckConstraint('unit_price >= 0', name='non_negative_unit_price'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_product_name'), 'products', ['product_name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('purchases',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('supermarket_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('total_amount', mysql.NUMERIC(), nullable=False),
    sa.ForeignKeyConstraint(['supermarket_id'], ['branches.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchases_supermarket_id'), 'purchases', ['supermarket_id'], unique=False)
    op.create_index(op.f('ix_purchases_user_id'), 'purchases', ['user_id'], unique=False)
    op.create_table('purchase_items',
    sa.Column('purchase_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.NUMERIC(), nullable=False),
    sa.CheckConstraint('quantity <= 1', name='max_quantity_per_product'),
    sa.CheckConstraint('quantity > 0', name='positive_quantity'),
    sa.CheckConstraint('unit_price >= 0', name='non_negative_unit_price'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('purchase_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchase_items')
    op.drop_index(op.f('ix_purchases_user_id'), table_name='purchases')
    op.drop_index(op.f('ix_purchases_supermarket_id'), table_name='purchases')
    op.drop_table('purchases')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_products_product_name'), table_name='products')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_branches_id'), table_name='branches')
    op.drop_table('branches')
    # ### end Alembic commands ###
