# Skill: engagement_manager

**Skill ID:** `engagement_manager`  
**Version:** 1.0.0  
**Last Updated:** 2026-02-05  
**Traceability:** SRS Section 4.4 (FR 4.0-4.2), specs/functional.md

## Description

Manages social media engagement including replies, comments, and interaction analysis. Used by Worker Agent to respond to audience interactions and build engagement.

## Use Case

Worker Agent invokes this skill when:
- New comments/replies need responses
- Engagement metrics need analysis
- Community management tasks are scheduled

## Input Contract

See `input_schema.json` for full JSON Schema definition.

**Example Input:**
```json
{
  "skill_name": "engagement_manager",
  "parameters": {
    "action": "reply",
    "platform": "instagram",
    "post_id": "post_12345",
    "comment_id": "comment_67890",
    "comment_text": "Love this look! Where can I get it?",
    "persona_id": "chimera_fashion_001"
  }
}
```

## Output Contract

See `output_schema.json` for full JSON Schema definition.

**Example Output:**
```json
{
  "response": {
    "text": "Thank you so much! 💕 Check the link in bio for all the details!",
    "action_taken": "reply",
    "platform_response_id": "resp_abc123"
  },
  "metadata": {
    "sentiment_detected": "positive",
    "persona_alignment": 0.95,
    "safety_score": 0.99,
    "response_time_ms": 850
  }
}
```

## Engagement Actions

| Action | Description |
|--------|-------------|
| `reply` | Reply to a comment |
| `like` | Like a comment or post |
| `analyze` | Analyze engagement metrics |
| `follow` | Follow a user |
| `dm` | Send direct message (requires HITL approval) |

## Safety Considerations

- DMs require HITL approval (confidence threshold: mandatory)
- Controversial topics flagged for review
- Rate limiting to avoid spam detection

## Implementation Status

⬜ Not implemented - TDD tests define the contract
