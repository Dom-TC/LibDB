"""The shelf database model."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libdb.database import db

if TYPE_CHECKING:
    from .book import Book


class Shelf(db.Model):  # type: ignore[name-defined]
    """The shelf database model."""

    __tablename__ = "shelves"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=None)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    books: Mapped[List["Book"]] = relationship(back_populates="shelf")
