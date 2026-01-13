"""Update models.

Revision ID: 1768273265
Revises: 1751899057
Create Date: 2026-01-13 03:01:05.500213

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1768273265"
down_revision: Union[str, Sequence[str], None] = "1751899057"
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_authors")),
        sa.UniqueConstraint("name", name=op.f("uq_authors_name")),
    )
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_genres")),
        sa.UniqueConstraint("name", name=op.f("uq_genres_name")),
    )
    op.create_table(
        "people",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_people")),
        sa.UniqueConstraint("name", name=op.f("uq_people_name")),
    )
    op.create_table(
        "publishers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_publishers")),
        sa.UniqueConstraint("name", name=op.f("uq_publishers_name")),
    )
    op.create_table(
        "series",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_series")),
        sa.UniqueConstraint("name", name=op.f("uq_series_name")),
    )
    op.create_table(
        "shelves",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shelves")),
        sa.UniqueConstraint("name", name=op.f("uq_shelves_name")),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("subtitle", sa.String(), nullable=True),
        sa.Column("volume", sa.String(), nullable=True),
        sa.Column("edition", sa.String(), nullable=True),
        sa.Column("publisher_id", sa.Integer(), nullable=True),
        sa.Column("published_date", sa.Date(), nullable=True),
        sa.Column("shelf_id", sa.Integer(), nullable=True),
        sa.Column(
            "read_status",
            sa.Enum("UNREAD", "READING", "READ", "DROPPED", name="bookreadstatus"),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["publisher_id"],
            ["publishers.id"],
            name=op.f("fk_books_publisher_id_publishers"),
        ),
        sa.ForeignKeyConstraint(
            ["shelf_id"], ["shelves.id"], name=op.f("fk_books_shelf_id_shelves")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
    )
    op.create_index(op.f("ix_books_title"), "books", ["title"], unique=False)
    op.create_table(
        "book_authors",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.Column("author_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
            name=op.f("fk_book_authors_author_id_authors"),
        ),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name=op.f("fk_book_authors_book_id_books")
        ),
        sa.PrimaryKeyConstraint("book_id", "author_id", name=op.f("pk_book_authors")),
    )
    op.create_table(
        "book_genres",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name=op.f("fk_book_genres_book_id_books")
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"], ["genres.id"], name=op.f("fk_book_genres_genre_id_genres")
        ),
        sa.PrimaryKeyConstraint("book_id", "genre_id", name=op.f("pk_book_genres")),
    )
    op.create_table(
        "book_loans",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.Column("loaned_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("returned_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name=op.f("fk_book_loans_book_id_books")
        ),
        sa.ForeignKeyConstraint(
            ["person_id"], ["people.id"], name=op.f("fk_book_loans_person_id_people")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_book_loans")),
    )
    op.create_index(
        op.f("ix_book_loans_book_id"), "book_loans", ["book_id"], unique=False
    )
    op.create_index(
        op.f("ix_book_loans_person_id"), "book_loans", ["person_id"], unique=False
    )
    op.create_index(
        "uq_active_loan_per_book",
        "book_loans",
        ["book_id"],
        unique=True,
        sqlite_where=sa.text("returned_at IS NULL"),
    )
    op.create_table(
        "book_series",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("series_id", sa.Integer(), nullable=False),
        sa.Column("series_position", sa.Float(), nullable=True),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name=op.f("fk_book_series_book_id_books")
        ),
        sa.ForeignKeyConstraint(
            ["series_id"], ["series.id"], name=op.f("fk_book_series_series_id_series")
        ),
        sa.PrimaryKeyConstraint("book_id", "series_id", name=op.f("pk_book_series")),
    )
    op.drop_table("book_author")
    op.drop_table("author")
    op.drop_table("book")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "book",
        sa.Column("title", sa.VARCHAR(), nullable=False),
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("subtitle", sa.VARCHAR(), nullable=True),
        sa.Column("volume", sa.VARCHAR(), nullable=True),
        sa.Column("edition", sa.VARCHAR(), nullable=True),
        sa.Column("publisher", sa.VARCHAR(), nullable=True),
        sa.Column("published", sa.VARCHAR(), nullable=True),
        sa.Column("location", sa.VARCHAR(), nullable=True),
        sa.Column("notes", sa.VARCHAR(), nullable=True),
        sa.Column("added", sa.VARCHAR(), nullable=True),
        sa.Column("has_read", sa.BOOLEAN(), nullable=True),
        sa.Column("genres", sa.VARCHAR(), nullable=True),
        sa.Column("is_lent_out", sa.BOOLEAN(), nullable=True),
        sa.Column("lent_to", sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "author",
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "book_author",
        sa.Column("book_id", sa.INTEGER(), nullable=False),
        sa.Column("author_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["author.id"],
        ),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
        ),
        sa.PrimaryKeyConstraint("book_id", "author_id"),
    )
    op.drop_table("book_series")
    op.drop_index(
        "uq_active_loan_per_book",
        table_name="book_loans",
        sqlite_where=sa.text("returned_at IS NULL"),
    )
    op.drop_index(op.f("ix_book_loans_person_id"), table_name="book_loans")
    op.drop_index(op.f("ix_book_loans_book_id"), table_name="book_loans")
    op.drop_table("book_loans")
    op.drop_table("book_genres")
    op.drop_table("book_authors")
    op.drop_index(op.f("ix_books_title"), table_name="books")
    op.drop_table("books")
    op.drop_table("shelves")
    op.drop_table("series")
    op.drop_table("publishers")
    op.drop_table("people")
    op.drop_table("genres")
    op.drop_table("authors")
