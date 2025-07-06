"""The config for the gunicorn server."""

import multiprocessing

bind = "127.0.0.1:8000"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
