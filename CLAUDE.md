# CLAUDE.md - Project Chimera

## Project Overview
This is **Project Chimera**, an autonomous influencer system for the AiQEM platform.
You are helping build the infrastructure ("Factory") that enables AI agents to create
and manage virtual influencers at scale.

## Prime Directive
🚨 **NEVER generate implementation code without checking specs/ first.**

All code must align with the specifications in:
- `specs/_meta.md` - Vision and constraints
- `specs/functional.md` - User stories and use cases
- `specs/technical.md` - API contracts, database schemas
- `specs/openclaw_integration.md` - Agent marketplace integration

## Architecture Pattern
This project uses the **FastRender Swarm pattern**:

```
Human Orchestrator
       ↓
   [Planner] ←→ Goals/Strategy
       ↓
   TaskQueue (Redis)
       ↓
   [Workers] ←→ MCP Tools
       ↓
   ReviewQueue (Redis)
       ↓
   [Judge] ←→ GlobalState
       ↓
   Approve / Reject / Escalate to Human
```

### Role Definitions:
- **Planner**: Decomposes high-level goals into executable task DAG
- **Worker**: Stateless executor of single atomic tasks (parallelizable)
- **Judge**: Validates quality, safety, and spec compliance

## Critical Constraints
1. **MCP-Only**: All external interactions MUST use Model Context Protocol
2. **Spec-First**: No implementation without corresponding specification
3. **TDD**: Write failing tests first, then implementation
4. **Traceability**: All sessions connected to Tenx MCP Sense

## Traceability Requirements
1. Always explain your plan BEFORE writing code
2. Break complex tasks into smaller steps
3. Reference spec sections when implementing features
4. Document assumptions and decisions

## Code Standards
- Python 3.11+
- PEP 8 style guidelines
- Type hints for ALL functions
- Docstrings for ALL public functions (Google style)
- Pydantic for data validation
- pytest for testing

## Testing Philosophy (TDD)
- Write tests BEFORE implementation
- Tests should initially FAIL (they define the goal)
- The AI agent "fills the slot" defined by failing tests
- Maintain >80% code coverage

## Directory Structure
```
project-chimera/
├── specs/           # 📋 Source of truth (READ FIRST!)
│   ├── _meta.md         # High-level vision
│   ├── functional.md    # User stories
│   ├── technical.md     # API contracts & schemas
│   └── openclaw_integration.md
├── skills/          # 🔧 Agent capabilities (I/O contracts)
│   ├── skill_fetch_trends/
│   ├── skill_download_youtube/
│   └── skill_transcribe_audio/
├── tests/           # ✅ TDD test files (FAILING first)
│   ├── test_trend_fetcher.py
│   ├── test_skills_interface.py
│   └── test_orchestrator.py
├── src/chimera/     # 🏗️ Implementation (after specs!)
├── research/        # 📚 Analysis documents
├── .cursor/rules    # 🤖 IDE context
└── CLAUDE.md        # 📖 This file
```

## MCP Integration
- All external interactions via Model Context Protocol
- **Resources**: Passive data sources (news://, twitter://, memory://)
- **Tools**: Executable functions (post_tweet, generate_image, send_transaction)
- **Prompts**: Reusable templates (persona_voice, safety_check)

## Skills vs Dev MCPs
Distinguish between:
- **Dev MCPs**: File writing, terminal execution, search (development time)
- **Runtime Skills**: Trend fetching, transcription, publishing (agent runtime)

Skills have formal I/O contracts documented in `skills/*/README.md`.

## Safety & HITL
Confidence-based routing:
- `> 0.90`: Auto-approve
- `0.70 - 0.90`: Human queue
- `< 0.70`: Reject/Retry
- Sensitive topics: ALWAYS human review

## Key Technologies
- Redis: Task queues, short-term memory
- Weaviate: Semantic/vector memory
- PostgreSQL/TimescaleDB: Structured data, time-series
- Coinbase AgentKit: Agentic commerce on Base network
- OpenClaw: Agent-to-agent marketplace

## Quick Reference Commands
```bash
make setup      # Install dependencies
make test       # Run tests (expect failures in TDD)
make spec-check # Verify spec alignment
make lint       # Run linters
make docker-up  # Start full stack
```

## When You're Unsure
1. Check specs/ directory first
2. Check skills/ for I/O contracts
3. Ask for clarification
4. Propose multiple options with trade-offs

## Skill Implementation Workflow
1. Read skill README in `skills/skill_name/README.md`
2. Note input/output TypeScript interfaces
3. Check corresponding test file in `tests/`
4. Implement to make tests pass
5. Update spec if contract changes
4. Reference the SRS document for detailed requirements
