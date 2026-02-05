# Trp1 Chimera

**Project Chimera** is the foundational infrastructure for an autonomous AI influencer network. This repository contains the "Agentic Operating System" designed to manage a fleet of AI agents that can research trends, generate content, and manage engagement without direct human intervention for every action.

## Getting Started

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started)
-   [Make](https://www.gnu.org/software/make/)
-   Python 3.11+ (for local setup)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Atnabon/trp1-chimera
    cd trp1-chimera
    ```

2.  **Set up the local environment:**
    This command creates a Python virtual environment and installs the dependencies listed in `pyproject.toml`. It prefers `uv` for speed but will fall back to `pip` if `uv` is not installed.
    ```bash
    make setup
    ```

## How to Run & Test with Docker

This project uses Docker to ensure a clean, consistent, and reliable testing environment. The primary way to run the project's test suite is via the `Makefile`.

**To run the tests:**

```bash
make test
```

**What this command does:**

1.  It builds a Docker image from the `Dockerfile`, installing all necessary dependencies in a clean environment.
2.  It runs the project's test suite (using `pytest`) inside a new container created from that image.

### Important: Expect Test Failures

This project follows a **Test-Driven Development (TDD)** methodology. The tests in the `tests/` directory have been written *before* the full implementation of the skills.

Therefore, when you run `make test`, you should expect to see **failing tests**. This is the correct and desired outcome at this stage. These failures define the "empty slots" that need to be filled by implementing the agent skills according to the project's specifications.


