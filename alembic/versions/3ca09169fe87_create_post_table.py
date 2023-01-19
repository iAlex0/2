"""create post table

Revision ID: 3ca09169fe87
Revises: 
Create Date: 2022-12-24 20:19:30.030073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ca09169fe87'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts')
