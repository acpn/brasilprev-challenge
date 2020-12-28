"""empty message

Revision ID: 3c7d31ef2ffd
Revises: 769d5875a08b
Create Date: 2020-11-23 12:59:09.966179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c7d31ef2ffd'
down_revision = '769d5875a08b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Product_price', table_name='Product')
    op.create_index(op.f('ix_Product_price'), 'Product', ['price'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Product_price'), table_name='Product')
    op.create_index('ix_Product_price', 'Product', ['price'], unique=True)
    # ### end Alembic commands ###