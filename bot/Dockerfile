FROM python:3.14.2-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv==0.7.13

# Copy bot dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy bot code
COPY bot.py ./
COPY config.py ./
COPY handlers/ ./handlers/
COPY services/ ./services/

# Run the bot
CMD ["uv", "run", "python", "bot.py"]
