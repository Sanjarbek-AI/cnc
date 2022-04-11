"""empty message

Revision ID: c2ab7009b2a4
Revises: 4a9dc7bbb310
Create Date: 2022-04-04 14:28:39.518648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2ab7009b2a4'
down_revision = '4a9dc7bbb310'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('competitions', sa.Column('code', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('competitions', 'code')
    # ### end Alembic commands ###
