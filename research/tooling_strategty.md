# Project Chimera - Tooling Strategy

## 1. Overview

This document outlines the tooling strategy for Project Chimera, distinguishing between:
- **Developer Tools (MCP)**: Tools that help YOU develop and debug
- **Agent Skills (Runtime)**: Capabilities the Chimera agents use in production

## 2. Developer Tools (MCP Servers)

### 2.1 Recommended MCP Servers for Development

| MCP Server | Purpose | Installation |
|------------|---------|--------------|
| `mcp-server-filesystem` | File read/write operations | `npx @anthropic-ai/mcp-server-filesystem` |
| `mcp-server-git` | Version control operations | `npx @anthropic-ai/mcp-server-git` |
| `mcp-server-sqlite` | Database queries for testing | `npx @anthropic-ai/mcp-server-sqlite` |
| `mcp-server-fetch` | HTTP requests for testing APIs | `npx @anthropic-ai/mcp-server-fetch` |

### 2.2 IDE Configuration

**.cursor/mcp.json** or **.vscode/mcp.json**:
```json
{
  "servers": {
    "tenxfeedbackanalytics": {
      "url": "https://mcppulse.10academy.org/proxy",
      "type": "http"
    },
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-server-filesystem", "/path/to/project"],
      "type": "stdio"
    },
    "git": {
      "command": "npx", 
      "args": ["@anthropic-ai/mcp-server-git"],
      "type": "stdio"
    }
  }
}
```

### 2.3 Tenx MCP Sense Integration

**Requirement:** Keep Tenx MCP Sense connected at all times.

Purpose:
- "Black Box" flight recorder for AI interactions
- Tracks thinking process for assessment
- Provides feedback analytics

## 3. Agent Skills (Runtime)

### 3.1 Skill Categories

```
skills/
├── content/
│   ├── skill_generate_caption/
│   ├── skill_generate_image/
│   └── skill_generate_video/
├── social/
│   ├── skill_post_twitter/
│   ├── skill_reply_comment/
│   └── skill_analyze_engagement/
├── research/
│   ├── skill_fetch_trends/
│   ├── skill_download_youtube/
│   └── skill_transcribe_audio/
├── commerce/
│   ├── skill_check_balance/
│   ├── skill_send_payment/
│   └── skill_create_invoice/
└── memory/
    ├── skill_store_memory/
    ├── skill_recall_memory/
    └── skill_update_persona/
```

### 3.2 Skill vs MCP Server

| Aspect | Skill | MCP Server |
|--------|-------|------------|
| **Scope** | Single capability | External bridge |
| **State** | Stateless | May maintain connections |
| **Caller** | Chimera Worker agents | Developer IDE or agents |
| **Example** | `skill_download_youtube` | `mcp-server-coinbase` |
| **Transport** | Python function call | JSON-RPC over stdio/SSE |

### 3.3 Critical Skills (MVP)

#### 1. skill_fetch_trends
- **Purpose**: Fetch trending topics from news/social
- **Input**: `{ "niche": "fashion", "region": "ethiopia", "limit": 10 }`
- **Output**: `{ "trends": [{"topic": "...", "score": 0.95}] }`

#### 2. skill_download_youtube
- **Purpose**: Download video for analysis
- **Input**: `{ "url": "https://youtube.com/...", "format": "audio" }`
- **Output**: `{ "file_path": "/tmp/video.mp3", "duration": 120 }`

#### 3. skill_transcribe_audio
- **Purpose**: Convert audio to text
- **Input**: `{ "file_path": "/tmp/video.mp3", "language": "en" }`
- **Output**: `{ "transcript": "...", "segments": [...] }`

## 4. Tool Selection Criteria

When choosing between building a skill vs using an MCP server:

| Criteria | Build Skill | Use MCP Server |
|----------|-------------|----------------|
| Single-purpose, atomic task | ✅ | |
| Needs external API bridge | | ✅ |
| High performance required | ✅ | |
| Shared across projects | | ✅ |
| Chimera-specific logic | ✅ | |
| Standard protocol (filesystem, git) | | ✅ |

## 5. Implementation Notes

### 5.1 Skill Interface Standard

Every skill MUST have:
1. `README.md` - Documentation
2. `schema.json` - Input/Output JSON Schema
3. `__init__.py` - Python implementation
4. `test_skill.py` - Unit tests

### 5.2 MCP Server Development

For custom MCP servers:
1. Use Python `mcp` SDK
2. Implement `@mcp.tool` decorators
3. Define `inputSchema` for all tools
4. Use stdio transport for local, SSE for remote

## 6. References

- [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [Anthropic MCP Servers](https://github.com/anthropics/mcp-servers)
- [Cursor MCP Documentation](https://docs.cursor.com/mcp)
