"""create user table

Revision ID: 1322b2000b87
Revises: 61d5b70148fe
Create Date: 2023-06-09 11:22:31.271782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1322b2000b87"
down_revision = "61d5b70148fe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
