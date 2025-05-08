# Base stage: Build with full Python and system deps
FROM python:3.12-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    QR_CODE_DIR=/myapp/qr_codes \
    PATH="/.venv/bin:$PATH"

WORKDIR /myapp

# Install system dependencies (now includes libzbar0 and libjpeg-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libc-bin \
    libzbar0 \
    libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN python -m venv /.venv \
    && /.venv/bin/pip install --upgrade pip \
    && /.venv/bin/pip install -r requirements.txt

# Final stage: Slim image for runtime
FROM python:3.12-slim-bookworm AS final

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    libc-bin \
    libzbar0 \
    libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    QR_CODE_DIR=/myapp/qr_codes \
    PATH="/.venv/bin:$PATH"

WORKDIR /myapp

# Add non-root user
RUN useradd -m myuser
USER myuser

# Copy venv and app code
COPY --from=base /.venv /.venv
COPY --chown=myuser:myuser . .

# Expose port
EXPOSE 8000

# Start the app
ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

