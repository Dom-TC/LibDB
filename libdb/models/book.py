"""The book database model."""

import enum
from datetime import date, datetime, timezone
from typing import List, Optional

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text, exists, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libdb.database import db

from .author import BookAuthor
from .genre import BookGenre
from .person import BookLoan
from .publisher import Publisher
from .series import BookSeries
from .shelf import Shelf


class BookReadStatus(enum.Enum):
    """Available options for a books reading status."""

    UNREAD = "unread"
    READING = "reading"
    READ = "read"
    DROPPED = "dropped"


class Book(db.Model):  # type: ignore[name-defined]
    """The book database model."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None)

    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    subtitle: Mapped[Optional[str]] = mapped_column(String, default=None)
    volume: Mapped[Optional[str]] = mapped_column(String, default=None)
    edition: Mapped[Optional[str]] = mapped_column(String, default=None)

    publisher_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("publishers.id"), default=None
    )
    published_date: Mapped[Optional[date]] = mapped_column(Date, default=None)

    shelf_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("shelves.id"), default=None
    )

    read_status: Mapped[BookReadStatus] = mapped_column(
        Enum(BookReadStatus),
        nullable=False,
        default=BookReadStatus.UNREAD,
    )

    notes: Mapped[Optional[str]] = mapped_column(Text, default=None)

    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    publisher: Mapped[Optional["Publisher"]] = relationship(back_populates="books")
    shelf: Mapped[Optional["Shelf"]] = relationship(back_populates="books")
    authors: Mapped[List["BookAuthor"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        order_by="BookAuthor.author_order",
    )
    genres: Mapped[List["BookGenre"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )
    series_entries: Mapped[List["BookSeries"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        order_by="BookSeries.series_position",
    )
    loans: Mapped[List["BookLoan"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )

    # Properties
    @property
    def active_loan(self) -> Optional["BookLoan"]:
        """The active BookLoan object, if any.

        Returns
        -------
        Optional[BookLoan]:
            The BookLoan object, if one exists.
        """
        return next(
            (loan for loan in self.loans if loan.returned_at is None),
            None,
        )

    @hybrid_property
    def is_loaned(self) -> bool:
        """Is the book currently loaned out.

        Returns
        -------
        bool
            Is the book currently loaned out?
        """
        return self.active_loan is not None

    @is_loaned.expression
    def _is_loaned_expr(cls):  # noqa N805
        from .person import BookLoan

        return (
            select(BookLoan.id)
            .where(
                BookLoan.book_id == cls.id,
                BookLoan.returned_at.is_(None),
            )
            .exists()
        )
