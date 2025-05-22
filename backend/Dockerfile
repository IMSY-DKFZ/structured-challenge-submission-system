## ------------------------------- Builder Stage ------------------------------ ## 
FROM python:3.13-bookworm AS builder
ENV TZ=Europe/Berlin 

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /app/src

COPY pyproject.toml .

RUN uv lock && uv sync --no-dev --no-install-project --frozen

## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.13-slim-bookworm AS prod
ENV TZ=Europe/Berlin 

WORKDIR /app/src
COPY alembic.ini .
COPY BMC_API BMC_API
COPY --from=builder /app/src/.venv .venv


# Set up environment variables for production
ENV PATH="/app/src/.venv/bin:$PATH"