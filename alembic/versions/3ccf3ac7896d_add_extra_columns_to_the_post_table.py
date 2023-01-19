"""add extra columns to the Post table

Revision ID: 3ccf3ac7896d
Revises: 23a6587a5966
Create Date: 2022-12-24 23:16:07.853760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ccf3ac7896d'
down_revision = '23a6587a5966'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE")),
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),)


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
