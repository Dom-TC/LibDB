"""Module for managing database connections."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """The base SQLAlchemy model."""

    metadata = MetaData(naming_convention=convention)

    def __repr__(self):
        """Generate a default __repr__ string for all subclasses."""
        try:
            state = inspect(self)
        except NoInspectionAvailable:
            return f"<{self.__class__.__name__}(uninspectable)>"

        attrs = []
        for c in state.mapper.column_attrs:
            value = state.dict.get(c.key, "<deferred>")
            attrs.append(f"{c.key}={value!r}")
        return f"<{self.__class__.__name__}({', '.join(attrs)})>"


db = SQLAlchemy(model_class=Base)


def init_db(app):
    """Create and setup the database."""
    # Initiate database
    app.logger.info("Initialising database")
    db.init_app(app)

    import libdb.models

    return db
