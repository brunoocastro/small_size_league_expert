# Python 3.12 image with uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Sync the project into a new environment, asserting the lockfile is up to date
RUN uv sync --locked

# Start the application
ENTRYPOINT ["uv", "run", "python", "discord_bot.py"] 