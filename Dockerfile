# Use the official Python 3.11 slim image as a base.
# This provides a lightweight environment.
FROM python:3.11-slim

# Set the working directory inside the container to /app.
WORKDIR /app

# Set environment variables for Python.
# PYTHONUNBUFFERED ensures that Python output is sent directly to the terminal.
# PYTHONPATH is set to the app directory to allow for absolute imports from the project root.
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install uv, a fast Python package installer, to speed up dependency installation.
RUN pip install uv

# Copy the dependency definition file. This is done separately to leverage Docker's layer
# caching. The dependencies will only be re-installed if pyproject.toml changes.
COPY pyproject.toml .

# Install project dependencies using uv.
# --system: Install packages into the system's Python environment.
# --no-cache: Disable caching to keep the image size smaller.
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy the rest of the project files into the working directory.
# Files and directories listed in .dockerignore will be excluded.
COPY . .

# Set the default command to run the pytest test suite when the container starts.
# This makes the container executable and its primary purpose clear: running tests.
CMD ["python", "-m", "pytest"]
