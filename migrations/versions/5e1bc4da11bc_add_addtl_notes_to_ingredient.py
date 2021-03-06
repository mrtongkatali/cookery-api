"""add addtl notes to ingredient

Revision ID: 5e1bc4da11bc
Revises: cbb7c0ceb1e1
Create Date: 2020-11-01 01:32:19.842514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e1bc4da11bc'
down_revision = 'cbb7c0ceb1e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredients', sa.Column('additional_note', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ingredients', 'additional_note')
    # ### end Alembic commands ###
