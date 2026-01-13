"""The various database models."""

from . import author, book, genre, person, publisher, series, shelf

Author = author.Author
BookAuthor = author.BookAuthor

Book = book.Book
BookReadStatus = book.BookReadStatus


Genre = genre.Genre
BookGenre = genre.BookGenre

Person = person.Person
BookLoan = person.BookLoan

Publisher = publisher.Publisher

Series = series.Series
BookSeries = series.BookSeries

Shelf = shelf.Shelf
