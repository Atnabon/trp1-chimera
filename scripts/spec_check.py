#!/usr/bin/env python3
"""
Project Chimera - Specification Validation Script

Validates that the project structure matches the specifications.
Reference: Challenge Document Task 3.2
"""

import os
import json
import sys
from pathlib import Path

# Required specification files
SPEC_FILES = [
    "specs/_meta.md",
    "specs/functional.md",
    "specs/technical.md",
    "specs/openclaw_integration.md",
]

# Required skills with schemas
SKILLS = [
    "trend_fetcher",
    "content_generator",
    "engagement_manager",
]

# Required test files
TEST_FILES = [
    "tests/test_trend_fetcher.py",
    "tests/test_skills_interface.py",
]

# Required infrastructure files
INFRA_FILES = [
    "Dockerfile",
    "Makefile",
    ".github/workflows/main.yml",
]


def check_spec_files() -> bool:
    """Check that all specification files exist."""
    all_exist = True
    for spec_file in SPEC_FILES:
        if not Path(spec_file).exists():
            print(f"  ✗ Missing: {spec_file}")
            all_exist = False
        else:
            print(f"  ✓ Found: {spec_file}")
    return all_exist


def check_skill_schemas() -> bool:
    """Check that all skills have input/output schemas."""
    all_valid = True
    for skill in SKILLS:
        skill_dir = Path(f"skills/{skill}")
        if not skill_dir.exists():
            print(f"  ✗ Missing skill directory: {skill_dir}")
            all_valid = False
            continue
        
        # Check for required schema files
        input_schema = skill_dir / "input_schema.json"
        output_schema = skill_dir / "output_schema.json"
        readme = skill_dir / "README.md"
        
        for schema_file in [input_schema, output_schema, readme]:
            if not schema_file.exists():
                print(f"  ✗ Missing: {schema_file}")
                all_valid = False
            else:
                print(f"  ✓ Found: {schema_file}")
                
        # Validate JSON schemas
        for schema_file in [input_schema, output_schema]:
            if schema_file.exists():
                try:
                    with open(schema_file, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    print(f"  ✗ Invalid JSON in {schema_file}: {e}")
                    all_valid = False
    
    return all_valid


def check_test_file_references() -> bool:
    """Check that test files exist and reference specs."""
    all_valid = True
    for test_file in TEST_FILES:
        if not Path(test_file).exists():
            print(f"  ✗ Missing: {test_file}")
            all_valid = False
        else:
            print(f"  ✓ Found: {test_file}")
            # Check for spec references in test file
            with open(test_file, 'r') as f:
                content = f.read()
                if "Reference:" not in content and "skills/" not in content:
                    print(f"  ⚠ Warning: {test_file} should reference specifications")
    return all_valid


def check_infra_files() -> bool:
    """Check that infrastructure files exist."""
    all_exist = True
    for infra_file in INFRA_FILES:
        if not Path(infra_file).exists():
            print(f"  ✗ Missing: {infra_file}")
            all_exist = False
        else:
            print(f"  ✓ Found: {infra_file}")
    return all_exist


def check_spec_meta_references() -> bool:
    """Check that _meta.md has proper structure."""
    meta_path = Path("specs/_meta.md")
    if not meta_path.exists():
        print("  ✗ _meta.md not found")
        return False
    
    with open(meta_path, 'r') as f:
        content = f.read()
    
    required_sections = [
        "Vision",
        "Architectural Constraints",
        "Quality Attributes",
    ]
    
    all_found = True
    for section in required_sections:
        if section.lower() not in content.lower():
            print(f"  ✗ Missing section: {section}")
            all_found = False
        else:
            print(f"  ✓ Found section: {section}")
    
    return all_found


def main():
    """Runs all validation checks and reports the final status."""
    print("=" * 60)
    print("  Project Chimera - Specification Validation")
    print("=" * 60)
    
    checks = {
        "Specification Files": check_spec_files,
        "Skill Schemas": check_skill_schemas,
        "Test Files": check_test_file_references,
        "Infrastructure Files": check_infra_files,
        "Meta Specification Structure": check_spec_meta_references,
    }

    all_passed = True
    for name, check_func in checks.items():
        print(f"\n[CHECKING] {name}...")
        if not check_func():
            all_passed = False
            print(f"[FAILED] {name}")
        else:
            print(f"[PASSED] {name}")

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All specification checks passed successfully!")
        sys.exit(0)
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
