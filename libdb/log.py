"""Configure logging."""

import logging
import logging.config
import os


def configure_logging():
    """Set up and configure logging."""
    # Set the log level based on the environment variable
    log = logging.getLogger(__name__)

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Configure logging
    logging.config.fileConfig(fname="log.conf", disable_existing_loggers=False)
    logging.getLogger().setLevel(numeric_level)

    # Configure file handlers
    if os.getenv("LOG_TO_FILE") == "false":
        log.info("LOG_TO_FILE is false, removing FileHandlers")
        file_handlers = (
            handler
            for handler in logging.root.handlers
            if isinstance(handler, logging.FileHandler)
        )
        for handler in file_handlers:
            logging.root.removeHandler(handler)
    elif os.getenv("LOG_FOLDER_PATH") is not None:
        log.info(f"Updating logging FileHandler path to {os.getenv('LOG_FOLDER_PATH')}")

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
        log.warning(
            f"LOG_TO_FILE is {os.getenv("LOG_TO_FILE")} but LOG_FOLDER_PATH is {os.getenv("LOG_FOLDER_PATH")}"
        )
