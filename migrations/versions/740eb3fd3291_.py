"""empty message

Revision ID: 740eb3fd3291
Revises: 7012ce2965c1
Create Date: 2020-07-25 21:11:59.718959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '740eb3fd3291'
down_revision = '7012ce2965c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dish', sa.Column('serving_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dish', 'serving_count')
    # ### end Alembic commands ###
