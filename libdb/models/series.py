"""The series database model."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libdb.database import db

if TYPE_CHECKING:
    from .book import Book


class Series(db.Model):  # type: ignore[name-defined]
    """The series database model."""

    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    books: Mapped[List["BookSeries"]] = relationship(
        back_populates="series", order_by="BookSeries.series_position"
    )


class BookSeries(db.Model):
    """The book_series database model."""

    __tablename__ = "book_series"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"), primary_key=True)

    series_position: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, default=None
    )
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    book: Mapped["Book"] = relationship(back_populates="series_entries")
    series: Mapped["Series"] = relationship(back_populates="books")
