ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy dependency files
COPY bot/pyproject.toml ./pyproject.toml
COPY uv.lock ./

# Install dependencies directly (no venv symlink issues)
RUN uv pip install --system -r pyproject.toml

# Copy bot code
COPY bot/bot.py ./
COPY bot/config.py ./
COPY bot/handlers/ ./handlers/
COPY bot/services/ ./services/

CMD ["python", "bot.py"]
