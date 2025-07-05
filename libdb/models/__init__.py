"""The various database models."""

from . import author, book
from .book_author import book_author as book_author_table

Book = book.Book
Author = author.Author
book_author = book_author_table
