"""add foreign key to post table

Revision ID: 375fb41e3b97
Revises: 1322b2000b87
Create Date: 2023-06-09 11:34:15.676851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "375fb41e3b97"
down_revision = "1322b2000b87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
