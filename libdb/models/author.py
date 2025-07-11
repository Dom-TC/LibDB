"""The author database model."""

from sqlalchemy.orm import Mapped, mapped_column

from libdb.database import db


class Author(db.Model):  # type: ignore[name-defined]
    """The author database model."""

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, default=None
    )

    books = db.relationship("Book", secondary="book_author", back_populates="authors")

    def __repr__(self) -> str:
        """Return the author name."""
        return f"<Author Name={self.name!r}>"
