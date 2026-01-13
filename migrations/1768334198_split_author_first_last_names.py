"""Split author first last names.

Revision ID: 1768334198
Revises: 1768273265
Create Date: 2026-01-13 19:56:38.537378

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1768334198"
down_revision: Union[str, Sequence[str], None] = "1768273265"
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema using batch mode for SQLite."""
    with op.batch_alter_table("authors") as batch_op:
        batch_op.add_column(sa.Column("first_names", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("surname", sa.String(), nullable=False))

        batch_op.drop_column("name")

        batch_op.create_unique_constraint(
            "uq_authors_full_name", ["first_names", "surname"]
        )

        batch_op.create_index("ix_authors_surname", ["surname"])


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("authors", sa.Column("name", sa.VARCHAR(), nullable=False))
    op.drop_index(op.f("ix_authors_surname"), table_name="authors")
    op.create_unique_constraint(op.f("uq_authors_name"), "authors", ["name"])
    op.drop_column("authors", "surname")
    op.drop_column("authors", "first_names")
