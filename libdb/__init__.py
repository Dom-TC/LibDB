"""App factory and entry point for libdb."""

import contextlib
import os

from dotenv import load_dotenv
from flask import Flask

from libdb.database import init_db
from libdb.models import Book

from . import default_config

load_dotenv()


# App factory as entry point to flask
def create_app(test_config=None):
    """App factory for setting up flask."""
    # Configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(default_config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_envvar("LIBDB_SETTINGS_FILE", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.config['DB_NAME']}"

    # Confirm the instance folder exists
    with contextlib.suppress(OSError):
        os.makedirs(app.instance_path)

    # Setup database
    db = init_db(app)

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        book = Book(
            title="The Name of the sdasas. dasdasde. asd",
            subtitle="The  Chronicle: Day One",
            publisher="DAW Books",
        )
        db.session.add(book)
        db.session.commit()

        return f'Hello, World! {app.config["SQLALCHEMY_DATABASE_URI"]} - {app.instance_path}'

    return app
