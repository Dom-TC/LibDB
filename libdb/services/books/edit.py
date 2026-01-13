"""Service for editing books."""

from datetime import date
from typing import List

from libdb.database import db
from libdb.models import (
    Author,
    Book,
    BookAuthor,
    BookGenre,
    BookSeries,
    Genre,
    Publisher,
    Series,
    Shelf,
)


def edit_book(
    book: Book,
    title: str,
    authors: List[Author],
    shelf: Shelf | None = None,
    publisher: Publisher | None = None,
    series: Series | None = None,
    series_position: int | None = None,
    genres: List[Genre] | None = None,
    subtitle: str | None = None,
    volume: str | None = None,
    edition: str | None = None,
    published_date: date | None = None,
    notes: str | None = None,
) -> Book:
    """Update an existing book and its relationships."""
    book.title = title
    book.subtitle = subtitle
    book.volume = volume
    book.edition = edition
    book.publisher = publisher
    book.shelf = shelf
    book.published_date = published_date
    book.notes = notes

    # Update Authors
    book.authors.clear()
    for i, author in enumerate(authors):
        ba = BookAuthor()
        ba.book_id = book.id
        ba.author_id = author.id
        ba.author_order = i

        db.session.add(ba)

    # Update Genres
    book.genres.clear()
    if genres:
        for genre in genres:
            bg = BookGenre()
            bg.book_id = book.id
            bg.genre_id = genre.id
            db.session.add(bg)

    # Update Series
    book.series_entries.clear()
    if series:
        bs = BookSeries()
        bs.book_id = book.id
        bs.series_id = series.id
        bs.series_position = series_position or 0
        db.session.add(bs)

    db.session.commit()
    return book
