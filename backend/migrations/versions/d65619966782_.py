"""empty message

Revision ID: d65619966782
Revises: b1795b07cde4
Create Date: 2019-05-18 15:35:52.336851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd65619966782'
down_revision = 'b1795b07cde4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('photo', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'photo')
    # ### end Alembic commands ###
