"""All views related to managing books / authors."""

from flask import Blueprint, flash, render_template
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from libdb.database import db
from libdb.forms import AddAuthorForm
from libdb.models import Author

bp = Blueprint("manage", __name__, url_prefix="/manage")


@bp.route("/add_author", methods=("GET", "POST"))
def add_author():
    """Add authors to the library."""
    add_author_form = AddAuthorForm()

    if add_author_form.validate_on_submit():
        author_name = (
            add_author_form.name.data.strip() if add_author_form.name.data else None
        )
        new_author = Author(name=author_name)  # type: ignore[call-arg]
        db.session.add(new_author)

        try:
            db.session.commit()
            flash(f"Successfully added {new_author.name}.")
        except IntegrityError:
            db.session.rollback()
            flash(f"Author '{new_author.name}' already exists.", "error")

    else:
        new_author = None

    return render_template(
        "manage/add_author.jinja", author=new_author, add_author_form=add_author_form
    )
