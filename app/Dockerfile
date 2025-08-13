# Use the uv base image with Python and uv preinstalled
FROM ghcr.io/astral-sh/uv:alpine

# Set the env variable to enable logs
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/local/app

# Copy the dependencie files (leverage docker laayer caching to avoid re-installing dependencies on every code change)
COPY pyproject.toml uv.lock ./

RUN uv sync

COPY ./ ./
