"""All views related to viewing the library."""

from flask import Blueprint, redirect, render_template, url_for

from libdb.data_handlers import clean_whitespace
from libdb.database import db
from libdb.forms import SearchForm
from libdb.models import Author, Book

bp = Blueprint("library", __name__, url_prefix=None)


@bp.route("/", methods=("GET", "POST"))
def index():
    """View the library."""
    form = SearchForm()

    # Join book and author tables
    query = db.session.query(Book).join(Book.authors)  # type: ignore[arg-type]

    if form.validate_on_submit():
        title = clean_whitespace(form.title)
        author = clean_whitespace(form.author)

        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))

        if author:
            query = query.filter(Author.name.ilike(f"%{author}%"))

        books = query.order_by(Author.name, Book.title).distinct().all()

    else:
        # Default listing all books
        books = query.order_by(Author.name, Book.title).distinct().all()

    return render_template("library/index.jinja", books=books, form=form)
