# SETUP STAGE
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS setup

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY app ./app

ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN uv sync --locked --no-dev


# RUNTIME STAGE
FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UVICORN_HOST=0.0.0.0 \
	UVICORN_PORT=8000 \
	PATH="/opt/venv/bin:$PATH"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends tini \
	&& rm -rf /var/lib/apt/lists/*

RUN groupadd --system appgroup \
	&& useradd --system --gid appgroup --create-home --home-dir /home/appuser appuser

WORKDIR /srv/app

COPY --from=setup /opt/venv /opt/venv
COPY --chown=appuser:appgroup app ./app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 --start-period=25s CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"UVICORN_PORT\", \"8000\")}/docs', timeout=2)"

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-m", "app"]
