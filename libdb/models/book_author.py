"""The book_author database model."""

from sqlalchemy import Column, ForeignKey

from libdb.database import db

book_author = db.Table(
    "book_author",
    Column("book_id", ForeignKey("book.id"), primary_key=True),
    Column("author_id", ForeignKey("author.id"), primary_key=True),
)
