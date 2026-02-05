# Trp1 Chimera

Project Chimera is an infrastructure project to build the "Factory" that creates **Autonomous AI Influencers** - a fleet of AI-powered virtual influencers capable of researching trends, generating content, and managing engagement at scale.

This repository contains the **specifications, tests, and tooling** required for AI agents (and humans) to build the final implementation using a spec-driven development approach.

## Getting Started

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started)
-   [Make](https://www.gnu.org/software/make/)
-   Python 3.11+ (for local setup)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Atnabon/trp1-chimera
cd project-chimera

# Setup environment
make setup

# Run tests (they will fail - TDD approach)
make test

# Run spec validation
make spec-check

# Start development services
make dev
```

## Development Philosophy

**"Intent (Specs) is the source of truth, Infrastructure (CI/CD, Tests, Docker) ensures reliability."**

1. **Spec-Driven Development**: No code without specifications
2. **Test-Driven Development**: Failing tests define requirements
3. **Traceability**: Tenx MCP Sense tracks all AI interactions
4. **Git Hygiene**: Commit early, commit often

## MCP Configuration

This project requires connection to Tenx MCP Sense for telemetry:

```json
{
  "mcpServers": {
    "tenxfeedbackanalytics": {
      "url": "https://mcppulse.10academy.org/proxy",
      "type": "http"
    }
  }
}
```

## Commands

```bash
# Development
make setup           # Create venv and install deps
make dev             # Start dev services (Redis, Postgres, Weaviate)
make test            # Run test suite
make test-cov        # Run tests with coverage

# Quality
make lint            # Run linters
make format          # Format code
make typecheck       # Type checking
make spec-check      # Validate specifications

# Docker
make docker-build    # Build all images
make docker-up       # Start full stack
make docker-down     # Stop services
make docker-logs     # View logs
```

