"""
Test suite for skills interface contracts.

Reference: skills/README.md
Traceability: Challenge Document Task 3.1, specs/technical.md

This file contains TDD tests that validate skill input/output contracts.
Tests are expected to FAIL until skills are implemented.
"""

import unittest
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Attempt to import skills (will fail until implemented)
try:
    from skills.trend_fetcher import fetch_trends
except ImportError:
    fetch_trends = None

try:
    from skills.content_generator import generate_content
except ImportError:
    generate_content = None

try:
    from skills.engagement_manager import manage_engagement
except ImportError:
    manage_engagement = None

# Load JSON schemas for validation
SKILLS_DIR = Path(__file__).parent.parent / "skills"


class TestSkillsDirectoryStructure(unittest.TestCase):
    """
    Test that skills directory has correct structure.
    
    Reference: skills/README.md
    Each skill must have: README.md, input_schema.json, output_schema.json
    """

    def test_skills_directory_exists(self):
        """Test that skills directory exists."""
        self.assertTrue(
            SKILLS_DIR.exists(),
            "skills/ directory must exist"
        )

    def test_trend_fetcher_structure(self):
        """Test trend_fetcher has required files."""
        skill_dir = SKILLS_DIR / "trend_fetcher"
        self.assertTrue(skill_dir.exists(), "trend_fetcher directory must exist")
        self.assertTrue((skill_dir / "README.md").exists())
        self.assertTrue((skill_dir / "input_schema.json").exists())
        self.assertTrue((skill_dir / "output_schema.json").exists())

    def test_content_generator_structure(self):
        """Test content_generator has required files."""
        skill_dir = SKILLS_DIR / "content_generator"
        self.assertTrue(skill_dir.exists(), "content_generator directory must exist")
        self.assertTrue((skill_dir / "README.md").exists())
        self.assertTrue((skill_dir / "input_schema.json").exists())
        self.assertTrue((skill_dir / "output_schema.json").exists())

    def test_engagement_manager_structure(self):
        """Test engagement_manager has required files."""
        skill_dir = SKILLS_DIR / "engagement_manager"
        self.assertTrue(skill_dir.exists(), "engagement_manager directory must exist")
        self.assertTrue((skill_dir / "README.md").exists())
        self.assertTrue((skill_dir / "input_schema.json").exists())
        self.assertTrue((skill_dir / "output_schema.json").exists())


class TestSkillsInputContracts(unittest.TestCase):
    """
    Test input contract validation for all skills.
    
    Reference: skills/*/input_schema.json
    Each skill must accept input matching its JSON schema.
    """

    def setUp(self):
        """Load input schemas for reference."""
        self.schemas = {}
        for skill_name in ["trend_fetcher", "content_generator", "engagement_manager"]:
            schema_path = SKILLS_DIR / skill_name / "input_schema.json"
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    self.schemas[skill_name] = json.load(f)

    def test_trend_fetcher_input_contract(self):
        """
        Test trend_fetcher input contract validation.
        
        Reference: skills/trend_fetcher/input_schema.json
        Required: skill_name="trend_fetcher", parameters.region, parameters.category
        """
        valid_input = {
            "skill_name": "trend_fetcher",
            "parameters": {
                "region": "ethiopia",
                "category": "fashion",
                "timeframe_hours": 24,
                "relevance_threshold": 0.75
            }
        }
        
        # This will fail until skill is implemented
        self.assertIsNotNone(
            fetch_trends,
            "fetch_trends function must be implemented in skills.trend_fetcher"
        )

    def test_content_generator_input_contract(self):
        """
        Test content_generator input contract validation.
        
        Reference: skills/content_generator/input_schema.json
        Required: skill_name="content_generator", parameters.content_type, parameters.platform, parameters.topic
        """
        valid_input = {
            "skill_name": "content_generator",
            "parameters": {
                "content_type": "multimodal",
                "platform": "instagram",
                "topic": "Sustainable Fashion Trends",
                "persona_constraints": ["Witty", "Sustainability-focused"],
                "tier": "hero"
            }
        }
        
        # This will fail until skill is implemented
        self.assertIsNotNone(
            generate_content,
            "generate_content function must be implemented in skills.content_generator"
        )

    def test_engagement_manager_input_contract(self):
        """
        Test engagement_manager input contract validation.
        
        Reference: skills/engagement_manager/input_schema.json
        Required: skill_name="engagement_manager", parameters.action, parameters.platform
        """
        valid_input = {
            "skill_name": "engagement_manager",
            "parameters": {
                "action": "reply",
                "platform": "instagram",
                "post_id": "post_12345",
                "comment_text": "Love this!",
                "persona_id": "chimera_001"
            }
        }
        
        # This will fail until skill is implemented
        self.assertIsNotNone(
            manage_engagement,
            "manage_engagement function must be implemented in skills.engagement_manager"
        )


class TestSkillsOutputContracts(unittest.TestCase):
    """
    Test output contract validation for all skills.
    
    Reference: skills/*/output_schema.json
    """

    def setUp(self):
        """Load output schemas for reference."""
        self.schemas = {}
        for skill_name in ["trend_fetcher", "content_generator", "engagement_manager"]:
            schema_path = SKILLS_DIR / skill_name / "output_schema.json"
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    self.schemas[skill_name] = json.load(f)

    def test_all_output_schemas_valid(self):
        """Test that all output schemas are valid JSON with required structure."""
        for skill_name, schema in self.schemas.items():
            with self.subTest(skill=skill_name):
                self.assertIn("$schema", schema, f"{skill_name} must have $schema")
                self.assertIn("properties", schema, f"{skill_name} must have properties")
                self.assertIn("required", schema, f"{skill_name} must have required fields")

    def test_trend_fetcher_output_has_metadata(self):
        """Test trend_fetcher output includes metadata."""
        if "trend_fetcher" in self.schemas:
            props = self.schemas["trend_fetcher"]["properties"]
            self.assertIn("metadata", props)

    def test_content_generator_output_has_content(self):
        """Test content_generator output includes content."""
        if "content_generator" in self.schemas:
            props = self.schemas["content_generator"]["properties"]
            self.assertIn("content", props)

    def test_engagement_manager_output_has_response(self):
        """Test engagement_manager output includes response."""
        if "engagement_manager" in self.schemas:
            props = self.schemas["engagement_manager"]["properties"]
            self.assertIn("response", props)


if __name__ == "__main__":
    unittest.main()
