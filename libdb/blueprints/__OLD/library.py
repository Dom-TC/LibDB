"""All views related to viewing the library."""

import logging

from flask import Blueprint, render_template, request

from libdb.database import db
from libdb.forms import SearchForm
from libdb.models import Author, Book

log = logging.getLogger(__name__)

bp = Blueprint("library", __name__, url_prefix=None)


@bp.route("/", methods=("GET", "POST"))
def index():
    """View the library."""
    form = SearchForm(request.args)

    # Join book and author tables
    query = db.session.query(Book).join(Book.authors)  # type: ignore[arg-type]

    if form.validate():
        title = request.args.get("title", "").strip()
        author = request.args.get("author", "").strip()

        search_terms = []

        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
            search_terms.append(f"title '{title}'")

        if author:
            query = query.filter(Author.name.ilike(f"%{author}%"))
            search_terms.append(f"author '{author}'")

        books = query.order_by(Author.name, Book.title).distinct().all()

        log.info(
            f"Searching for {' and '.join(search_terms) if search_terms else 'all books'}"
        )
        log.info(f"Found {len(books)} result{'s' if len(books) > 1 else ''}")

    else:
        # Default listing all books
        books = query.order_by(Author.name, Book.title).distinct().all()

    book_count = len(books)
    if book_count == 1:
        result_count = "1 Result"
    else:
        result_count = f"{book_count} Results"

    return render_template(
        "library/index.jinja", books=books, result_count=result_count, form=form
    )
