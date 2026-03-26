ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy dependency files first for better caching
COPY bot/pyproject.toml ./pyproject.toml
COPY uv.lock ./

# Install dependencies with cache mount for faster builds
RUN --mount=type=cache,target=/home/uv/.cache/uv,sharing=locked \
    uv pip install --system -r pyproject.toml

# Copy bot code
COPY bot/bot.py ./
COPY bot/config.py ./
COPY bot/handlers/ ./handlers/
COPY bot/services/ ./services/

CMD ["python", "bot.py"]
