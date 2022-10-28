"""add subscription channel table

Revision ID: 358e2db2c8f4
Revises: a56f3ef13254
Create Date: 2022-10-28 10:03:05.067589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '358e2db2c8f4'
down_revision = 'a56f3ef13254'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscription_etag', sa.Text(), nullable=False),
    sa.Column('subscription_id', sa.Text(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('published_at', sa.DateTime(), nullable=True),
    sa.Column('resource_kind', sa.String(length=30), nullable=True),
    sa.Column('resource_channel_id', sa.String(length=30), nullable=False),
    sa.Column('snippet_channel_id', sa.String(length=30), nullable=False),
    sa.Column('thumbnails_default_url', sa.Text(), nullable=True),
    sa.Column('thumbnails_medium_url', sa.Text(), nullable=True),
    sa.Column('thumbnails_high_url', sa.Text(), nullable=True),
    sa.Column('total_item_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('resource_channel_id'),
    sa.UniqueConstraint('subscription_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscription_channels')
    # ### end Alembic commands ###
