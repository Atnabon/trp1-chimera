# Skill: content_generator

**Skill ID:** `content_generator`  
**Version:** 1.0.0  
**Last Updated:** 2026-02-05  
**Traceability:** SRS Section 4.3 (FR 3.0-3.3), specs/functional.md US-005, US-006

## Description

Generates multi-modal content (text, image, video) based on trends and persona constraints. Used by Worker Agent to create social media posts tailored to specific platforms and personas.

## Use Case

Worker Agent invokes this skill when:
- A content generation task is popped from TaskQueue
- Planner has identified a trend worth creating content for
- Scheduled posting requires new content

## Input Contract

See `input_schema.json` for full JSON Schema definition.

**Example Input:**
```json
{
  "skill_name": "content_generator",
  "parameters": {
    "content_type": "multimodal",
    "platform": "instagram",
    "topic": "Sustainable Fashion Trends",
    "persona_constraints": ["Witty", "Sustainability-focused"],
    "character_reference_id": "agent-123-character-lora",
    "tier": "hero",
    "budget_limit_usdc": 25.00
  }
}
```

## Output Contract

See `output_schema.json` for full JSON Schema definition.

**Example Output:**
```json
{
  "content": {
    "text": "Fashion that loves the planet! 🌿 Check out these eco-friendly looks...",
    "media_urls": ["https://storage.chimera.ai/images/gen_abc123.png"],
    "media_type": "image",
    "hashtags": ["#SustainableFashion", "#EcoStyle"]
  },
  "metadata": {
    "generation_id": "gen_abc123",
    "persona_alignment": 0.92,
    "safety_score": 0.98,
    "cost_usdc": 2.50,
    "generation_time_ms": 4500
  }
}
```

## Content Tiers

| Tier | Description | Typical Cost |
|------|-------------|-------------|
| `filler` | Quick engagement posts | $0.05-0.20 |
| `regular` | Standard quality content | $0.50-2.00 |
| `hero` | High-quality campaign content | $5.00-25.00 |

## MCP Tools Used

- `generate_text` - LLM text generation
- `generate_image` - Image synthesis
- `generate_video` - Video generation (hero tier)

## Implementation Status

⬜ Not implemented - TDD tests define the contract
