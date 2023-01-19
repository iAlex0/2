"""add content column to post table

Revision ID: 730c5374d818
Revises: 3ca09169fe87
Create Date: 2022-12-24 22:31:37.404382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '730c5374d818'
down_revision = '3ca09169fe87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
