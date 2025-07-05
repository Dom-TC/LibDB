"""A form to add authors to the library."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddAuthorForm(FlaskForm):
    """A form to add authors to the library."""

    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add Author")
