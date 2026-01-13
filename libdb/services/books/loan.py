"""Services for loaning and returning books."""

from datetime import datetime, timezone

from libdb.database import db
from libdb.models import Book, BookLoan, Person


def loan_book(book: Book, person: Person) -> BookLoan:
    """Create a new loan for the given book and person."""
    # Ensure book is not already loaned
    if book.active_loan:
        raise ValueError(
            f"Book {book.title} is already loaned to {book.active_loan.person.name}."
        )

    loan = BookLoan()
    loan.book = book
    loan.person = person
    loan.loaned_at = datetime.now(timezone.utc)

    db.session.add(loan)
    db.session.commit()
    return loan


def return_book(book: Book) -> BookLoan | None:
    """Return the currently active loan for the book."""
    active = book.active_loan
    if not active:
        return None

    active.returned_at = datetime.now(timezone.utc)
    db.session.commit()
    return active
