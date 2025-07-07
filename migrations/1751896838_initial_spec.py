"""Initial spec.

Revision ID: 1751896072
Revises:
Create Date: 2025-07-07 14:47:52.494462

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1751896072"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = ("default",)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "author",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "book",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("subtitle", sa.String(), nullable=True),
        sa.Column("volume", sa.String(), nullable=True),
        sa.Column("edition", sa.String(), nullable=True),
        sa.Column("publisher", sa.String(), nullable=True),
        sa.Column("published", sa.String(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("added", sa.String(), nullable=True),
        sa.Column("has_read", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )

    op.create_table(
        "book_author",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["author.id"],
        ),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
        ),
        sa.PrimaryKeyConstraint("book_id", "author_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("book_author")
    op.drop_table("book")
    op.drop_table("author")
