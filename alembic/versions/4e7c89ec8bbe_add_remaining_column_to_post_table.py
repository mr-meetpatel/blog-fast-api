"""add remaining column to post table

Revision ID: 4e7c89ec8bbe
Revises: 375fb41e3b97
Create Date: 2023-06-09 11:40:40.696528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4e7c89ec8bbe"
down_revision = "375fb41e3b97"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "is_published")
    op.drop_column("posts", "created_at")
