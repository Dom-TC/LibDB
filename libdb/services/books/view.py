"""Service for viewing book details."""

from typing import Optional

from libdb.database import db
from libdb.models import Book


def get_book_by_id(book_id: int) -> Optional[Book]:
    """
    Retrieve a book by its ID, including related authors, genres, series, shelf, and publisher.

    Returns None if the book does not exist.
    """
    return (
        db.session.query(Book)
        .filter(Book.id == book_id)
        .options(
            db.selectinload(Book.authors).selectinload("author"),
            db.selectinload(Book.genres).selectinload("genre"),
            db.selectinload(Book.series_entries).selectinload("series"),
            db.selectinload(Book.shelf),
            db.selectinload(Book.publisher),
            db.selectinload(Book.loans).selectinload("person"),
        )
        .one_or_none()
    )
