"""Form for loaning a book to a person using QuerySelectField."""

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from libdb.models import Person


class LoanBookForm(FlaskForm):
    """Select a person to loan a book to."""

    person = QuerySelectField(
        "Person",
        query_factory=lambda: Person.query.order_by(Person.name).all(),
        get_label="name",
        allow_blank=False,
        validators=[DataRequired()],
    )

    submit = SubmitField("Loan Book")
