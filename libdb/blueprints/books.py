"""Books blueprint and routes."""

from collections import defaultdict

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from libdb.forms.books import AddBookForm, LoanBookForm
from libdb.models import Book
from libdb.services.books import (
    BookSort,
    LoanFilter,
    ReadFilter,
    SortDirection,
    add_book,
    edit_book,
    get_book_by_id,
    list_books,
    loan_book,
    return_book,
)
from libdb.services.shelves import list_shelves

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

    shelves: dict[str, list[Book]] = defaultdict(list)

    all_shelves = list_shelves()

    for shelf in all_shelves:
        shelves[shelf.name] = []

    for book in books:
        shelf_name = book.shelf.name if book.shelf else "Unsorted"
        shelves[shelf_name].append(book)

    return render_template(
        "/books/list.jinja",
        shelves=shelves,
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
        book = add_book(
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
        return redirect(url_for("books.list_books_route"))

    return render_template("books/add.jinja", form=form)


@bp.route("/<int:book_id>", methods=["GET"])
def view_book_route(book_id: int):
    """View the details of a specified book."""
    book = get_book_by_id(book_id)
    if not book:
        abort(404, description=f"Book with ID {book_id} not found")

    return render_template("books/view.jinja", book=book)


@bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book_route(book_id: int):
    """Edit the details for a specified book."""
    book = Book.query.get_or_404(book_id)
    form = AddBookForm(obj=book)

    if form.validate_on_submit():
        edit_book(
            book=book,
            title=form.title.data or "",
            subtitle=form.subtitle.data,
            volume=form.volume.data,
            edition=form.edition.data,
            publisher=form.get_or_create_publisher(),
            shelf=form.shelf.data,
            published_date=form.published_date.data,
            notes=form.notes.data,
            authors=form.authors.data,
            series=form.get_or_create_series(),
            series_position=form.series_position.data,
            genres=form.get_or_create_genres(),
        )
        flash("Book updated successfully.", "success")
        return redirect(url_for("books.view_book_route", book_id=book.id))

    # Refresh choices
    form.__init__(obj=book)

    return render_template("books/edit.jinja", form=form, book=book)


@bp.route("/<int:book_id>/loan", methods=["GET", "POST"])
def loan_book_route(book_id: int):
    """Loan the specified book to a person."""
    book = Book.query.get_or_404(book_id)
    form = LoanBookForm()

    if form.validate_on_submit():
        person = form.person.data

        try:
            loan_book(book, person)
            flash(f"{book.title} loaned to {person.name}.", "success")
        except ValueError as e:
            flash(str(e), "warning")
        return redirect(url_for("books.view_book_route", book_id=book.id))

    return render_template("books/loan.jinja", form=form, book=book)


@bp.route("/<int:book_id>/return", methods=["POST"])
def return_book_route(book_id: int):
    """Return a loaned out book."""
    book = Book.query.get_or_404(book_id)
    loan = return_book(book)
    if loan:
        flash(f"{book.title} has been returned by {loan.person.name}.", "success")
    else:
        flash(f"{book.title} is not currently loaned out.", "warning")
    return redirect(url_for("books.view_book_route", book_id=book.id))
