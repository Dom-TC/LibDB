"""Module for managing database connections."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    """Extended by all database models."""

    pass


db = SQLAlchemy(model_class=Base)


def init_db(app):
    """Create and setup the database."""
    # Initiate database
    app.logger.info("Initialising database")
    db.init_app(app)

    # Import models
    from libdb.models.author import Author
    from libdb.models.book import Book
    from libdb.models.book_author import book_author

    return db
