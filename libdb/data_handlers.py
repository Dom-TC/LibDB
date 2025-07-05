"""Assorted utilities for handling and modifying data."""


def clean_whitespace(field):
    """Remove excess whitespace around string."""
    return field.data.strip() if field.data else None
