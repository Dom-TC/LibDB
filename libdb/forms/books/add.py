"""Forms to add a new book."""

from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from libdb.database import db
from libdb.models import Author, Genre, Publisher, Series, Shelf


class AddBookForm(FlaskForm):
    """Form to add a new book."""

    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[Optional()])
    volume = StringField("Volume", validators=[Optional()])
    edition = StringField("Edition", validators=[Optional()])

    # Publishers
    publisher = QuerySelectField(
        "Publisher",
        query_factory=lambda: Publisher.query.order_by(Publisher.name).all(),
        get_label="name",
        allow_blank=True,
        validators=[Optional()],
    )
    new_publisher_name = StringField("Or add a new Publisher", validators=[Optional()])

    # Series
    series = QuerySelectField(
        "Series",
        query_factory=lambda: Series.query.order_by(Series.name).all(),
        get_label="name",
        allow_blank=True,
        validators=[Optional()],
    )
    new_series_name = StringField("Or add a new Series", validators=[Optional()])
    series_position = IntegerField("Series Position", validators=[Optional()])

    # Shelf
    shelf = QuerySelectField(
        "Shelf",
        query_factory=lambda: Shelf.query.order_by(Shelf.name).all(),
        get_label="name",
        allow_blank=True,
        validators=[Optional()],
    )

    # Authors
    authors = QuerySelectMultipleField(
        "Authors",
        query_factory=lambda: Author.query.order_by(
            Author.surname, Author.first_names
        ).all(),
        get_label=lambda a: f"{a.surname}, {a.first_name}",
        allow_blank=False,
        validators=[DataRequired()],
    )

    # Genres
    genres = QuerySelectMultipleField(
        "Genres",
        query_factory=lambda: Genre.query.order_by(Genre.name).all(),
        get_label="name",
        allow_blank=True,
        validators=[Optional()],
    )
    new_genre_names = StringField(
        "Add new Genres (comma-separated)", validators=[Optional()]
    )

    published_date = DateField("Published Date", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])

    submit = SubmitField("Add Book")

    # ------------------------------------------------------------------------
    # Helper methods to create new entities if needed
    # ------------------------------------------------------------------------
    def get_or_create_publisher(self) -> Publisher | None:
        """Return selected publisher or create a new one."""
        if self.new_publisher_name.data:
            pub = Publisher.query.filter_by(name=self.new_publisher_name.data).first()
            if not pub:
                pub = Publisher()
                pub.name = self.new_publisher_name.data
                db.session.add(pub)
                db.session.commit()
            return pub
        return self.publisher.data

    def get_or_create_series(self) -> Series | None:
        """Return selected series or create a new one."""
        if self.new_series_name.data:
            series = Series.query.filter_by(name=self.new_series_name.data).first()
            if not series:
                series = Series()
                series.name = self.new_series_name.data
                db.session.add(series)
                db.session.commit()
            return series
        return self.series.data

    def get_or_create_genres(self) -> list[Genre]:
        """Return list of selected genres plus any new genres."""
        genres = list(self.genres.data)  # existing selections

        if self.new_genre_names.data:
            genre_names = [
                n.strip() for n in self.new_genre_names.data.split(",") if n.strip()
            ]
            for genre_name in genre_names:
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    genre = Genre()
                    genre.name = genre_name
                    db.session.add(genre)
                    db.session.commit()
                genres.append(genre)
        return genres
