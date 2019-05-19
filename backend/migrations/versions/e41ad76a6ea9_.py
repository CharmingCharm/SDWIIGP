"""empty message

Revision ID: e41ad76a6ea9
Revises: 83935c1432e9
Create Date: 2019-05-19 15:48:32.409680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e41ad76a6ea9'
down_revision = '83935c1432e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submission', sa.Column('full_score', sa.DECIMAL(precision=6, scale=2), nullable=True))
    op.add_column('submission', sa.Column('score', sa.DECIMAL(precision=6, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('submission', 'score')
    op.drop_column('submission', 'full_score')
    # ### end Alembic commands ###
