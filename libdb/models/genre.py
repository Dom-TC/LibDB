"""The genre database model."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libdb.database import db

if TYPE_CHECKING:
    from .book import Book


class Genre(db.Model):  # type: ignore[name-defined]
    """The book database model."""

    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    books: Mapped[List["BookGenre"]] = relationship(back_populates="genre")


class BookGenre(db.Model):
    """The book_genre database model."""

    __tablename__ = "book_genres"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    book: Mapped["Book"] = relationship(back_populates="genres")
    genre: Mapped["Genre"] = relationship(back_populates="books")
