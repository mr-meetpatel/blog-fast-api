"""add content column to post table

Revision ID: 61d5b70148fe
Revises: baa7ae9cb8e8
Create Date: 2023-06-09 11:15:35.359350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61d5b70148fe"
down_revision = "baa7ae9cb8e8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
