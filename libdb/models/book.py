"""The book database model."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from libdb.database import db


class Book(db.Model):  # type: ignore[name-defined]
    """The book database model."""

    title: Mapped[str]
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, default=None
    )
    subtitle: Mapped[Optional[str]] = mapped_column(default=None)
    volume: Mapped[Optional[str]] = mapped_column(default=None)
    edition: Mapped[Optional[str]] = mapped_column(default=None)
    publisher: Mapped[Optional[str]] = mapped_column(default=None)
    published: Mapped[Optional[str]] = mapped_column(default=None)
    location: Mapped[Optional[str]] = mapped_column(default=None)
    notes: Mapped[Optional[str]] = mapped_column(default=None)
    added: Mapped[Optional[str]] = mapped_column(default=datetime.now())
    has_read: Mapped[Optional[bool]] = mapped_column(default=False)
    genres: Mapped[Optional[str]] = mapped_column(default=None)

    authors = db.relationship("Author", secondary="book_author", back_populates="books")

    def __repr__(self) -> str:
        """Return book title and publisher."""
        return f"<Book title={self.title!r} publisher={self.publisher!r}>"
