"""Books services."""

from enum import StrEnum


class BookSort(StrEnum):
    DEFAULT = "default"
    TITLE = "title"
    AUTHOR = "author"
    SERIES = "series"


class SortDirection(StrEnum):
    ASC = "asc"
    DSC = "DSC"


class ReadFilter(StrEnum):
    ALL = "all"
    READ = "read"
    UNREAD = "unread"


class LoanFilter(StrEnum):
    ALL = "all"
    LOANED = "loaned"
    AVAILABLE = "available"
