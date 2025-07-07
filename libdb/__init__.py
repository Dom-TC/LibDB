"""App factory and entry point for libdb."""

import contextlib
import logging
import logging.config
import os
import secrets

from dotenv import load_dotenv
from flask import Flask
from flask_alembic import Alembic

from libdb.blueprints import library_blueprint, manage_blueprint
from libdb.database import init_db

from . import default_config

load_dotenv()


# App factory as entry point to flask
def create_app(test_config=None):
    """App factory for setting up flask."""
    # Set the log level based on the environment variable
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Configure logging
    logging.config.fileConfig(fname="log.conf", disable_existing_loggers=False)
    logging.getLogger().setLevel(numeric_level)

    # Configure file handlers
    if os.getenv("LOG_TO_FILE") == "false":
        logging.info("LOG_TO_FILE is false, removing FileHandlers")
        file_handlers = (
            handler
            for handler in logging.root.handlers
            if isinstance(handler, logging.FileHandler)
        )
        for handler in file_handlers:
            logging.root.removeHandler(handler)
    elif os.getenv("LOG_FOLDER_PATH") is not None:
        logging.info(
            f"Updating logging FileHandler path to {os.getenv('LOG_FOLDER_PATH')}"
        )

        file_handlers = (
            handler
            for handler in logging.root.handlers
            if isinstance(handler, logging.FileHandler)
        )
        for handler in file_handlers:
            handler.stream.close()
            handler.baseFilename = os.path.abspath(
                f"{os.getenv('LOG_FOLDER_PATH')}/log"
            )
            handler.stream = handler._open()
    else:
        logging.warning(
            f"LOG_TO_FILE is {os.getenv("LOG_TO_FILE")} but LOG_FOLDER_PATH is {os.getenv("LOG_FOLDER_PATH")}"
        )

    log = logging.getLogger(__name__)

    log.info("Starting libdb")

    # Configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(default_config)

    # Confirm the instance folder exists
    with contextlib.suppress(OSError):
        os.makedirs(app.instance_path)

    # Generate SECRET_KEY if it doesn't already exist and load it
    app.config.from_pyfile("secret_key_config.cfg", silent=True)

    if app.config["SECRET_KEY"]:
        app.logger.info("Found SECRET_KEY")
    else:
        app.logger.warning("Couldn't find SECRET_KEY. Generating...")

        secret_config_path = os.path.join(app.instance_path, "secret_key_config.cfg")
        with open(secret_config_path, "w") as f:
            f.write(f'SECRET_KEY = "{secrets.token_hex()}"')

        app.config.from_pyfile("secret_key_config.cfg", silent=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.logger.info(f"Loading config from {os.getenv("LIBDB_SETTINGS_FILE")}")
        app.config.from_envvar("LIBDB_SETTINGS_FILE", silent=True)
    else:
        # load the test config if passed in
        app.logger.info("Loading test_config")
        app.config.from_mapping(test_config)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.config['DB_NAME']}"
    app.logger.info(f"Database: {app.config["SQLALCHEMY_DATABASE_URI"]}")

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
    app.register_blueprint(library_blueprint)
    app.register_blueprint(manage_blueprint)

    app.add_url_rule("/", endpoint="index")

    return app
