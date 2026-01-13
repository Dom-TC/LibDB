"""App factory and entry point for libdb."""

import contextlib
import logging
import os
from typing import Any, Mapping

from dotenv import load_dotenv
from flask import Flask
from flask_alembic import Alembic

from libdb.blueprints import books_bp
from libdb.config import configure_app
from libdb.database import init_db
from libdb.log import configure_logging

load_dotenv()
log = logging.getLogger(__name__)


# App factory as entry point to flask
def create_app(test_config: Mapping[str, Any] | None = None):
    """App factory for setting up flask."""
    app = Flask(__name__, instance_relative_config=True)

    # Confirm the instance folder exists
    with contextlib.suppress(OSError):
        os.makedirs(app.instance_path)

    configure_logging()
    configure_app(app, test_config)

    log.info("Starting libdb")

    # Setup database
    db = init_db(app)  # noqa: F841

    # Register alembic
    app.logger.info("Registering alembic")
    alembic = Alembic()
    alembic.init_app(app)

    with app.app_context():
        app.logger.info("Attempting to upgrade database")
        alembic.upgrade()

    app.logger.info("Registering blueprints")
    app.register_blueprint(books_bp)

    app.add_url_rule("/", endpoint="index")

    return app
