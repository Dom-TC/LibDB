"""Add lent out.

Revision ID: 1751899057
Revises: 1751898042
Create Date: 2025-07-07 15:37:37.196285

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1751899057"
down_revision: Union[str, Sequence[str], None] = "1751898042"
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("book", sa.Column("is_lent_out", sa.Boolean(), nullable=True))
    op.add_column("book", sa.Column("lent_to", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("book", "lent_to")
    op.drop_column("book", "is_lent_out")
