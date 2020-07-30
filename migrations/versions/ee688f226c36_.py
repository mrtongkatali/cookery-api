"""empty message

Revision ID: ee688f226c36
Revises: 
Create Date: 2020-07-26 03:08:05.941260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee688f226c36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('firstname', sa.String(length=20), nullable=False),
    sa.Column('lastname', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('dish',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dish_name', sa.String(length=100), nullable=True),
    sa.Column('main_dish', sa.Integer(), nullable=True),
    sa.Column('course', sa.Integer(), nullable=True),
    sa.Column('cuisine', sa.Integer(), nullable=True),
    sa.Column('prep_hour', sa.Integer(), nullable=True),
    sa.Column('prep_minute', sa.Integer(), nullable=True),
    sa.Column('cook_hour', sa.Integer(), nullable=True),
    sa.Column('cook_minute', sa.Integer(), nullable=True),
    sa.Column('serving_count', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_profile',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photoFsRef', sa.String(length=50), nullable=True),
    sa.Column('short_bio', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nutrition_facts',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dish_id', sa.Integer(), nullable=False),
    sa.Column('nutrition_label', sa.String(length=50), nullable=True),
    sa.Column('nutrition_value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['dish_id'], ['dish.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prep_instruction',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dish_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('step_order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dish_id'], ['dish.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prep_instruction')
    op.drop_table('nutrition_facts')
    op.drop_table('user_profile')
    op.drop_table('dish')
    op.drop_table('user')
    # ### end Alembic commands ###