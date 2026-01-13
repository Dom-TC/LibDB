"""Configure app."""

import os
import secrets
from typing import Any, Mapping

from flask import Flask

from . import default_config


def configure_app(app: Flask, test_config: Mapping[str, Any] | None = None):
    """Configure the app."""
    app.logger.info("Configuring libdb")

    app.config.from_object(default_config)

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
