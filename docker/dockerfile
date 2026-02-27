FROM python:3.12-slim

# Installing UV
COPY --from=ghcr.io/astral-sh/uv:0.5.6 /uv /uvx /bin/

# Tell uv to install dependencies directly into the system (e.g. not create a venv)
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Change working directory
WORKDIR /app

# Copy pyproject.toml file
COPY pyproject.toml pyproject.toml

# Installing dependencies
RUN uv sync

# Copying project files. Since project files change less often w.r.t. dependencies, they are put after installation in
# order to exploit layers cache.
COPY src/ src/
COPY main.py main.py

# Start server
CMD ["python", "main.py"]

