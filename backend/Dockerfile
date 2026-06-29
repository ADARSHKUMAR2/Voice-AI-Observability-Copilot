FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first to leverage Docker caching
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-cache

# Copy the rest of the backend source code
COPY . .

EXPOSE 5001

# Execute the FastAPI server inside the uv virtual environment
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]