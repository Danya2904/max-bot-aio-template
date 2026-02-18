# Use Python 3.10 slim as base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if they exist (assuming user will add them to pyproject.toml or requirements.txt)
# For now, we'll install the core dependencies directly to ensure the image builds
RUN pip install --no-cache-dir \
    aiohttp \
    sqlalchemy[asyncio] \
    asyncpg \
    redis \
    pydantic-settings \
    pydantic

# Copy the rest of the application code
COPY . .

# Command to run the bot
CMD ["python", "app/main.py"]
