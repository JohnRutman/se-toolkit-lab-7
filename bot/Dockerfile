ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

WORKDIR /app

# Copy the pre-built virtual environment and code
COPY bot/.venv ./.venv
COPY bot/bot.py ./
COPY bot/config.py ./
COPY bot/handlers/ ./handlers/
COPY bot/services/ ./services/
COPY bot/pyproject.toml ./

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "bot.py"]
