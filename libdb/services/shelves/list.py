"""Service for listing shelves."""

import logging
from typing import Sequence

from sqlalchemy import asc, case, desc, select
from sqlalchemy.orm import joinedload

from libdb.database import db
from libdb.models import (
    Author,
    Book,
    BookAuthor,
    BookLoan,
    BookReadStatus,
    BookSeries,
    Series,
    Shelf,
)

log = logging.getLogger(__name__)


def list_shelves() -> Sequence[Shelf]:
    """Return a list of shelves."""
    stmt = select(Shelf).order_by(Shelf.name).distinct()

    return db.session.scalars(stmt).unique().all()
