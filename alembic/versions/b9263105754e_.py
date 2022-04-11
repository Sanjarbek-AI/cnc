"""empty message

Revision ID: b9263105754e
Revises: 
Create Date: 2022-04-04 12:37:11.321947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9263105754e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competition_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('competition_id', sa.Integer(), nullable=True),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('user_code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competitions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_uz', sa.String(), nullable=True),
    sa.Column('image_ru', sa.String(), nullable=True),
    sa.Column('conditions_uz', sa.Text(), nullable=True),
    sa.Column('conditions_ru', sa.Text(), nullable=True),
    sa.Column('gifts_uz', sa.Text(), nullable=True),
    sa.Column('gifts_ru', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_uz', sa.String(), nullable=True),
    sa.Column('image_ru', sa.String(), nullable=True),
    sa.Column('contact_uz', sa.Text(), nullable=True),
    sa.Column('contact_ru', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('like', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('showrooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_uz', sa.String(), nullable=True),
    sa.Column('image_ru', sa.String(), nullable=True),
    sa.Column('info_uz', sa.Text(), nullable=True),
    sa.Column('info_ru', sa.Text(), nullable=True),
    sa.Column('location_link', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('showrooms')
    op.drop_table('posts')
    op.drop_table('contacts')
    op.drop_table('competitions')
    op.drop_table('competition_user')
    # ### end Alembic commands ###
