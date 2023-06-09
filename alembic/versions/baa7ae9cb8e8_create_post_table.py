"""create post table

Revision ID: baa7ae9cb8e8
Revises: 
Create Date: 2023-06-09 11:04:48.459164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "baa7ae9cb8e8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title",sa.String(),nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts')
