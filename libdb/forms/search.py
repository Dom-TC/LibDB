"""A form to search for existing books in the library."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    """A form to search for existing books based on either a title and/or an author."""

    title = StringField("Title")
    author = StringField("Author")
    submit = SubmitField("Search")
