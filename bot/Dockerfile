ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

# Copy bot dependencies
COPY bot/pyproject.toml ./pyproject.toml
COPY uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy bot code
COPY bot/bot.py ./
COPY bot/config.py ./
COPY bot/handlers/ ./handlers/
COPY bot/services/ ./services/

# Sync again to install the project
RUN uv sync --frozen

# ---
# Runtime stage
# ---
ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Copy the application from the builder
COPY --from=builder /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

CMD ["python", "bot.py"]
