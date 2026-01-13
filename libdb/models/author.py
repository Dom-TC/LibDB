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

    first_names: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False, index=True)

    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    books: Mapped[List["BookAuthor"]] = relationship(back_populates="author")

    # Properties
    @property
    def display_name(self) -> str:
        """Return formatted name: 'Surname, First Name'."""
        return f"{self.surname}, {self.first_names}"


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
