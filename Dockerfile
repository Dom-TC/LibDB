FROM python:3.13.5-slim AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl=8.7.1 && \
    rm -rf /var/lib/apt/lists/*


FROM base AS final

LABEL org.opencontainers.image.source=https://github.com/Dom-TC/LibDB

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.1.3 \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PATH="/root/.local/bin:/app/.venv/bin:$PATH"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN :8.7.1 -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY libdb ./libdb

RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction

COPY log.conf gunicorn.conf.py ./
COPY logs ./logs

RUN adduser --disabled-password --gecos '' libdb && \
    chown -R libdb:libdb /app

USER libdb

CMD ["gunicorn", "libdb:create_app()", "--config", "gunicorn.conf.py"]
