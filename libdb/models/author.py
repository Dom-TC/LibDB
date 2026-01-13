"""The author database model."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libdb.database import db

if TYPE_CHECKING:
    from .book import Book


class Author(db.Model):  # type: ignore[name-defined]
    """The author database model."""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None)

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    books: Mapped[List["BookAuthor"]] = relationship(back_populates="author")


class BookAuthor(db.Model):  # type: ignore[name-defined]
    """The book_author database model."""

    __tablename__ = "book_authors"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    author_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    book: Mapped["Book"] = relationship(back_populates="authors")
    author: Mapped["Author"] = relationship(back_populates="books")
