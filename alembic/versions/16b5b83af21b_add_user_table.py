"""add users table

Revision ID: 16b5b83af21b
Revises: f168c2899cd4
Create Date: 2025-03-01 18:52:06.666379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16b5b83af21b'
down_revision: Union[str, None] = 'f168c2899cd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('saved_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.Column('in_shopping_cart', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'product_id', name='unique_user_product')
    )
    op.create_index(op.f('ix_saved_products_id'), 'saved_products', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_saved_products_id'), table_name='saved_products')
    op.drop_table('saved_products')
    # ### end Alembic commands ###
