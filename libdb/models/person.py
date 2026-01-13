"""The person database model."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libdb.database import db

if TYPE_CHECKING:
    from .book import Book


class Person(db.Model):  # type: ignore[name-defined]
    """The person database model."""

    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    loans: Mapped[List["BookLoan"]] = relationship(back_populates="person")


class BookLoan(db.Model):  # type: ignore[name-defined]
    """Tracks book lending history."""

    __tablename__ = "book_loans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None)

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False,
        index=True,
    )

    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"),
        nullable=False,
        index=True,
    )

    loaned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    returned_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None,
    )

    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    book: Mapped["Book"] = relationship(back_populates="loans")
    person: Mapped["Person"] = relationship(back_populates="loans")

    __table_args__ = (
        Index(
            "uq_active_loan_per_book",
            "book_id",
            unique=True,
            sqlite_where=returned_at.is_(None),
        ),
    )
