# Skill: trend_fetcher

**Skill ID:** `trend_fetcher`  
**Version:** 1.0.0  
**Last Updated:** 2026-02-05  
**Traceability:** SRS Section 4.2 (FR 2.0-2.2), specs/functional.md US-003

## Description

Fetches and analyzes trending topics from multiple sources (news, social media, market data) via MCP Resources. Used by Planner Agent to discover relevant trends for content creation campaigns.

## Use Case

Planner Agent invokes this skill when:
- Campaign goals require trend awareness
- Periodic trend monitoring is scheduled
- User requests trend analysis for a specific region/category

## Input Contract

See `input_schema.json` for full JSON Schema definition.

**Example Input:**
```json
{
  "skill_name": "trend_fetcher",
  "parameters": {
    "region": "ethiopia",
    "category": "fashion",
    "timeframe_hours": 24,
    "relevance_threshold": 0.75
  }
}
```

## Output Contract

See `output_schema.json` for full JSON Schema definition.

**Example Output:**
```json
{
  "trends": [
    {
      "topic": "Sustainable Fashion",
      "engagement_score": 0.87,
      "growth_rate": "+15%",
      "sources": ["mcp://news/ethiopia/fashion", "mcp://twitter/trends"],
      "relevance_score": 0.92
    }
  ],
  "metadata": {
    "fetched_at": "2026-02-05T10:30:00Z",
    "source_count": 3,
    "confidence": 0.89
  }
}
```

## MCP Resources Used

- `news://{region}/{category}` - News articles
- `twitter://trends/{region}` - Twitter trending topics
- `reddit://r/{subreddit}/hot` - Reddit hot posts

## Error Handling

- Rate limits → Retry with exponential backoff
- Source unavailable → Continue with other sources, reduce confidence
- No trends found → Return empty array with low confidence

## Implementation Status

⬜ Not implemented - TDD tests define the contract
