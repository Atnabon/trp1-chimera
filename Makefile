# Makefile for Project Chimera

# --- Variables ---
PYTHON_INTERPRETER := $(shell command -v python3 || command -v python)
VENV_DIR := venv
IMAGE_NAME := chimera-agent-factory
IMAGE_TAG := latest

# --- Phony Targets ---
.PHONY: all help setup test test-local spec-check docker-build docker-test clean lint format typecheck dev

# --- Main Targets ---

all: help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo "  setup         Initializes the local development environment."
	@echo "  test          Builds the Docker image and runs tests inside the container."
	@echo "  test-local    Runs tests using the local Python environment."
	@echo "  test-cov      Runs tests with coverage report."
	@echo "  spec-check    Validates the project's specification files and structure."
	@echo "  docker-build  Builds the Docker image."
	@echo "  docker-test   Runs tests inside a pre-built Docker container."
	@echo "  lint          Runs linters (ruff)."
	@echo "  format        Formats code with ruff."
	@echo "  typecheck     Runs type checking with mypy."
	@echo "  dev           Starts development services."
	@echo "  clean         Removes temporary files and the virtual environment."
	@echo "  help          Displays this help message."

# setup: Creates a virtual environment and installs dependencies.
setup:
	@echo "--> Setting up local development environment..."
	@if command -v uv >/dev/null; then \
		echo "--> 'uv' found. Using uv for setup."; \
		uv venv $(VENV_DIR) && uv pip install -e ".[dev]"; \
	else \
		echo "--> 'uv' not found. Falling back to standard venv and pip."; \
		$(PYTHON_INTERPRETER) -m venv $(VENV_DIR) && \
		. $(VENV_DIR)/bin/activate && \
		pip install --upgrade pip && \
		pip install -e ".[dev]"; \
	fi
	@echo "--> Setup complete. Activate the environment with: source $(VENV_DIR)/bin/activate"

# test-local: Runs the pytest suite in the local environment.
test-local:
	@echo "--> Running tests locally..."
	@$(PYTHON_INTERPRETER) -m pytest tests/ -v

# test-cov: Runs tests with coverage report.
test-cov:
	@echo "--> Running tests with coverage..."
	@$(PYTHON_INTERPRETER) -m pytest tests/ -v --cov=src --cov-report=term-missing

# spec-check: Executes the script to validate project specifications.
spec-check:
	@echo "--> Validating project specifications..."
	@$(PYTHON_INTERPRETER) scripts/spec_check.py

# lint: Run linters
lint:
	@echo "--> Running linters..."
	@$(PYTHON_INTERPRETER) -m ruff check src/ tests/

# format: Format code
format:
	@echo "--> Formatting code..."
	@$(PYTHON_INTERPRETER) -m ruff format src/ tests/

# typecheck: Run type checking
typecheck:
	@echo "--> Running type checking..."
	@$(PYTHON_INTERPRETER) -m mypy src/

# dev: Start development services (placeholder)
dev:
	@echo "--> Starting development services..."
	@echo "Note: Redis, Postgres, Weaviate services would start here"
	@echo "For now, run: docker-compose up -d"

# --- Docker Targets ---

docker-build:
	@echo "--> Building Docker image: $(IMAGE_NAME):$(IMAGE_TAG)..."
	@docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-test:
	@echo "--> Running tests inside Docker container..."
	@docker run --rm $(IMAGE_NAME):$(IMAGE_TAG) python -m pytest tests/ -v

# test: The primary test command for CI. It builds the image and runs tests inside it.
test: docker-build docker-test

# --- Utility Targets ---

clean:
	@echo "--> Cleaning up project artifacts..."
	@rm -rf $(VENV_DIR) .pytest_cache .mypy_cache .ruff_cache
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "--> Cleanup complete."
