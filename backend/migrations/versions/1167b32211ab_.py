"""empty message

Revision ID: 1167b32211ab
Revises: 8c475eb11e86
Create Date: 2019-05-17 18:11:44.533464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1167b32211ab'
down_revision = '8c475eb11e86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcement',
    sa.Column('aid', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['uid'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('aid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('announcement')
    # ### end Alembic commands ###
