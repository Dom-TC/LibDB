"""Books service."""

from . import add, edit, enums
from . import list as _list
from . import loan, view

BookSort = enums.BookSort
SortDirection = enums.SortDirection
ReadFilter = enums.ReadFilter
LoanFilter = enums.LoanFilter

list_books = _list.list_books
add_book = add.add_book
get_book_by_id = view.get_book_by_id
edit_book = edit.edit_book
loan_book = loan.loan_book
return_book = loan.return_book
