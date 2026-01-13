"""Service for listing books."""

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
)

from .enums import BookSort, LoanFilter, ReadFilter, SortDirection


def list_books(
    *,
    sort: BookSort = BookSort.DEFAULT,
    direction: str = SortDirection.ASC,
    read_filter: ReadFilter = ReadFilter.ALL,
    loan_filter: LoanFilter = LoanFilter.ALL,
    shelf_id: int | None = None,
) -> Sequence[Book]:
    """Return a list of books filtered and sorted according to the given criteria."""
    stmt = (
        select(Book)
        .options(
            joinedload(Book.shelf),
            joinedload(Book.publisher),
            joinedload(Book.authors).joinedload(BookAuthor.author),
            joinedload(Book.series_entries).joinedload(BookSeries.series),
        )
        .distinct()
    )

    stmt = _apply_read_filter(stmt, read_filter)
    stmt = _apply_loan_filter(stmt, loan_filter)
    stmt = _apply_shelf_filter(stmt, shelf_id)

    if sort == BookSort.DEFAULT:
        stmt = _apply_default_sort(stmt)
    else:
        stmt = _apply_sort(stmt, sort, direction)

    return db.session.scalars(stmt).unique().all()


def _apply_read_filter(stmt, read_filter: ReadFilter):
    if read_filter == ReadFilter.READ:
        return stmt.where(Book.read_status == BookReadStatus.READ)
    elif read_filter == ReadFilter.UNREAD:
        return stmt.where(Book.read_status != BookReadStatus.READ)
    return stmt


def _apply_shelf_filter(stmt, shelf_id: int | None):
    if shelf_id is not None:
        return stmt.where(Book.shelf_id == shelf_id)
    return stmt


def _apply_loan_filter(stmt, loan_filter: LoanFilter):
    if loan_filter == LoanFilter.ALL:
        return stmt

    active_loan = (
        select(BookLoan.id)
        .where(
            BookLoan.book_id == Book.id,
            BookLoan.returned_at.is_(None),
        )
        .exists()
    )

    if loan_filter == LoanFilter.LOANED:
        return stmt.where(active_loan)
    elif loan_filter == LoanFilter.AVAILABLE:
        return stmt.where(~active_loan)

    return stmt


def _apply_sort(stmt, sort: BookSort, direction: str):
    order = asc if direction == "asc" else desc

    if sort == BookSort.TITLE:
        return stmt.order_by(order(Book.title))
    elif sort == BookSort.AUTHOR:
        stmt = stmt.join(Book.authors).join(BookAuthor.author)
        return stmt.order_by(
            order(Author.surname), order(Author.first_names), order(Book.title)
        )
    elif sort == BookSort.SERIES:
        stmt = stmt.join(Book.series_entries).join(BookSeries.series)
        return stmt.order_by(order(Series.name), order(BookSeries.series_position))
    return stmt


def _apply_default_sort(stmt):
    """Apply the default sort.

    Hierarchy:
      1. Shelf
      2. Primary author surname, first name
      3. Series first (series name -> series_position)
      4. Standalone books by title
    """
    stmt = (
        stmt.join(Book.authors)
        .join(BookAuthor.author)
        .outerjoin(Book.series_entries)
        .outerjoin(BookSeries.series)
    )

    # Primary author only
    stmt = stmt.where(BookAuthor.author_order == 0)

    # Series vs standalone
    has_series = case({BookSeries.series_id.isnot(None): 0}, else_=1)

    stmt = stmt.order_by(
        Book.shelf_id,
        Author.surname,
        Author.first_names,
        has_series,
        Series.name.nullsfirst(),
        BookSeries.series_position.nullsfirst(),
        Book.title,
    )

    return stmt
