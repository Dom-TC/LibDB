"""Books blueprint and routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from libdb.forms import AddBookForm
from libdb.services.books import (
    BookSort,
    LoanFilter,
    ReadFilter,
    SortDirection,
)
from libdb.services.books import add_book as service_add_book
from libdb.services.books import (
    list_books,
)

bp = Blueprint(
    "books",
    __name__,
    url_prefix="/books",
)


@bp.route("/", methods=["GET"])
def list_books_route():
    """List all books with optional filters and sorting."""
    sort = BookSort(request.args.get("sort", BookSort.DEFAULT))
    direction = SortDirection(request.args.get("dir", SortDirection.ASC))

    read = ReadFilter(request.args.get("read", ReadFilter.ALL))
    loan = LoanFilter(request.args.get("loan", LoanFilter.ALL))
    shelf_id = request.args.get("shelf")

    books = list_books(
        sort=sort,
        direction=direction,
        read_filter=read,
        loan_filter=loan,
        shelf_id=int(shelf_id) if shelf_id else None,
    )

    return render_template(
        "/books/list.jinja",
        books=books,
        sort=sort,
        direction=direction,
        read=read,
        loan=loan,
        shelf_id=shelf_id,
        BookSort=BookSort,
        ReadFilter=ReadFilter,
        LoanFilter=LoanFilter,
    )


@bp.route("/add", methods=["GET", "POST"])
def add_book_route():
    """Add a new book."""
    form = AddBookForm()

    if form.validate_on_submit():
        book = service_add_book(
            title=form.title.data or "",
            authors=form.authors.data,
            shelf=form.shelf.data,
            publisher=form.get_or_create_publisher(),
            series=form.get_or_create_series(),
            series_position=form.series_position.data,
            genres=form.get_or_create_genres(),
            subtitle=form.subtitle.data,
            volume=form.volume.data,
            edition=form.edition.data,
            published_date=form.published_date.data,
            notes=form.notes.data,
        )
        flash(f"Added book {book.title}", "success")
        return redirect(url_for("books.list_books"))

    return render_template("books/add.jinja", form=form)


@bp.route("/<int:book_id>", methods=["GET"])
def view_book(book_id: int):
    """View the details of a specified book."""
    pass


@bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id: int):
    """Edit the details for a specified book."""
    pass


@bp.route("/<int:book_id>/loan", methods=["GET", "POST"])
def loan_book(book_id: int):
    """Loan the specified book to a person."""
    pass


@bp.route("/<int:book_id>/return", methods=["POST"])
def return_book(book_id: int):
    """Return a loaned out book."""
    pass


@bp.route("/series", methods=["GET"])
def list_series():
    """List all series."""
    pass


@bp.route("/series/<int:series_id>/edit", methods=["GET", "POST"])
def edit_series(series_id: int):
    """Edit the specified series."""
    pass


@bp.route("/<int:book_id>/series/add", methods=["POST"])
def add_book_to_series(book_id: int):
    """Add the specified book to a series."""
    pass


@bp.route("/<int:book_id>/series/remove", methods=["POST"])
def remove_book_from_series(book_id: int):
    """Remove a book from a series."""
    pass
