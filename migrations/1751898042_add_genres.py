"""Add genres.

Revision ID: 1751898042
Revises: 1751896072
Create Date: 2025-07-07 15:20:42.232301

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1751898042"
down_revision: Union[str, Sequence[str], None] = "1751896072"
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("book", sa.Column("genres", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("book", "genres")
