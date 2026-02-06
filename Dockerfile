# Project Chimera - Dockerfile
# Multi-stage build for production deployment

# =============================================================================
# Stage 1: Builder
# =============================================================================
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
WORKDIR /app
COPY pyproject.toml ./
COPY requirements*.txt ./

# Install dependencies from requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# =============================================================================
# Stage 2: Runtime
# =============================================================================
FROM python:3.11-slim as runtime

# Labels
LABEL maintainer="Chimera Team" \
    version="0.1.0" \
    description="Project Chimera - Autonomous Influencer Network"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH" \
    # Application settings
    ENVIRONMENT=production \
    LOG_LEVEL=INFO

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # For healthchecks
    curl \
    # For media processing (ffmpeg for audio/video)
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd --gid 1000 chimera && \
    useradd --uid 1000 --gid 1000 --create-home chimera

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=chimera:chimera . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/exports && \
    chown -R chimera:chimera /app

# Switch to non-root user
USER chimera

# Expose ports
# 8000 - API server
# 8001 - MCP server
# 9090 - Metrics
EXPOSE 8000 8001 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - can be overridden
CMD ["python", "-m", "chimera.main"]

# =============================================================================
# Stage 3: Development (optional)
# =============================================================================
FROM runtime as development

# Switch to root to install dev tools
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install dev Python packages
RUN pip install ipython ipdb pytest-watch

# Switch back to chimera user
USER chimera

# Development command with auto-reload
CMD ["python", "-m", "chimera.main", "--reload"]

# =============================================================================
# Stage 4: Worker
# =============================================================================
FROM runtime as worker

# Worker-specific configuration
ENV WORKER_TYPE=default \
    WORKER_CONCURRENCY=5 \
    WORKER_PREFETCH=1

# Worker command
CMD ["python", "-m", "chimera.worker"]

# =============================================================================
# Stage 5: Judge
# =============================================================================
FROM runtime as judge

# Judge-specific configuration
ENV JUDGE_MODEL=gemini-2.0-flash \
    JUDGE_BATCH_SIZE=10

# Judge command
CMD ["python", "-m", "chimera.judge"]
