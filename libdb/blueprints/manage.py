"""All views related to managing books / authors."""

import logging

from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from libdb.data_handlers import clean_whitespace
from libdb.database import db
from libdb.forms import AddAuthorForm, AddBookForm
from libdb.models import Author, Book

log = logging.getLogger(__name__)

bp = Blueprint("manage", __name__, url_prefix="/manage")


@bp.route("/add_author", methods=("GET", "POST"))
def add_author():
    """Add authors to the library."""
    form = AddAuthorForm()

    if form.validate_on_submit():
        author_name = clean_whitespace(form.name)
        new_author = Author(name=author_name)  # type: ignore[call-arg]

        log.info(f"Adding author: {new_author.name}")

        db.session.add(new_author)

        try:
            db.session.commit()
            flash(f"Successfully added {new_author.name}.")
            log.info(f"Successfully added author: {new_author.name}. Redirecting.")
            return redirect(url_for("manage.add_author"))
        except IntegrityError:
            db.session.rollback()
            log.info(f"Failed to add author: {new_author.name} already exists.")
            flash(f"Author '{new_author.name}' already exists.", "error")

    else:
        new_author = None

    return render_template("manage/add_author.jinja", author=new_author, form=form)


@bp.route("/add_book", methods=("GET", "POST"))
def add_book():
    """Add books to the library."""
    form = AddBookForm()

    if form.validate_on_submit():
        title = clean_whitespace(form.title)
        subtitle = clean_whitespace(form.subtitle)
        volume = clean_whitespace(form.volume)
        edition = clean_whitespace(form.edition)
        publisher = clean_whitespace(form.publisher)
        location = clean_whitespace(form.location)
        notes = clean_whitespace(form.notes)

        published = form.published.data
        has_read = form.has_read.data

        selected_authors = form.authors.data

        new_book = Book(
            title=title,  # type: ignore[call-arg]
            subtitle=subtitle,  # type: ignore[call-arg]
            volume=volume,  # type: ignore[call-arg]
            edition=edition,  # type: ignore[call-arg]
            publisher=publisher,  # type: ignore[call-arg]
            published=published,  # type: ignore[call-arg]
            location=location,  # type: ignore[call-arg]
            notes=notes,  # type: ignore[call-arg]
            has_read=has_read,  # type: ignore[call-arg]
        )

        new_book.authors = selected_authors

        log.info(f"Adding book: {new_book.title}")

        db.session.add(new_book)

        try:
            db.session.commit()
            log.info(f"Successfully added author: {new_book.title}. Redirecting.")
            flash(f"Successfully added {new_book.title}.")
            return redirect(url_for("manage.add_book"))
        except IntegrityError:
            db.session.rollback()
            flash("Failed to add book due to database error.", "error")
            log.info(f"Failed to add book: {new_book.title}.")

    else:
        new_book = None

    return render_template("manage/add_book.jinja", book=new_book, form=form)
