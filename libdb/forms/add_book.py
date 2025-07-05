"""A form to add a new book to the library."""

from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from libdb.models import Author


class AddBookForm(FlaskForm):
    """A form to add a new book to the library."""

    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle")

    authors = QuerySelectMultipleField(
        "Authors",
        query_factory=lambda: Author.query.order_by(Author.name).all(),
        get_label="name",
        allow_blank=False,
        validators=[DataRequired()],
    )

    volume = StringField("Volume")
    edition = StringField("Edition")
    publisher = StringField("Publisher")
    published = DateField("Published", validators=[Optional()])
    location = StringField("Location")
    notes = TextAreaField("Notes")
    has_read = BooleanField("Read?")

    submit = SubmitField("Add Book")
