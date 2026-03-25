FROM python:3.14.2-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv==0.7.13

# Copy bot dependencies
COPY bot/pyproject.toml ./pyproject.toml
COPY uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy bot code
COPY bot/bot.py ./
COPY bot/config.py ./
COPY bot/handlers/ ./handlers/
COPY bot/services/ ./services/

# Run the bot
CMD ["uv", "run", "python", "bot.py"]
