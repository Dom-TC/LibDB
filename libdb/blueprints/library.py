"""All views related to library management."""

from flask import Blueprint, render_template
from sqlalchemy.orm import joinedload

from libdb.database import db
from libdb.forms import SearchForm
from libdb.models import Author, Book

bp = Blueprint("library", __name__, url_prefix=None)


@bp.route("/", methods=("GET", "POST"))
def index():
    """View the library."""
    search_form = SearchForm()

    # Join book and author tables
    query = db.session.query(Book).join(Book.authors)  # type: ignore[arg-type]

    if search_form.validate_on_submit():
        print("validated.")
        title = search_form.title.data.strip() if search_form.title.data else None
        author = search_form.author.data.strip() if search_form.author.data else None

        print(f"title:  {title}")
        print(f"author: {author}")
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))

        if author:
            query = query.filter(Author.name.ilike(f"%{author}%"))

        books = query.order_by(Author.name, Book.title).distinct().all()

    else:
        # Default listing all books
        books = query.order_by(Author.name, Book.title).distinct().all()

    return render_template("library/index.html", books=books, search_form=search_form)
