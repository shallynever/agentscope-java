---
name: JSON Validator
description: Validates JSON strings for correct syntax and structure. Use this skill to check if a JSON string is well-formed or matches a specific schema.
skill-id: json-validator_filesystem-resources_skills
---

# JSON Validator Skill

This skill provides functionality to validate JSON strings against syntax rules and optional JSON schemas.

## Usage

1. Load the skill:
```python
validator = load_skill_through_path(
    skillId="json-validator_filesystem-resources_skills",
    path="SKILL.md"
)
```

2. Validate a JSON string:
```python
result = validator.validate('{"key": "value"}')
if result["valid"]:
    print("Valid JSON")
else:
    print(f"Invalid JSON: {result['error']}")
```

3. Optional: Validate against a JSON schema
```python
schema = {...}  # Your JSON schema
data = '{"key": "value"}'
result = validator.validate(data, schema=schema)
```

## Implementation Details

The validation uses Python's `json` module for syntax checking. Schema validation requires the `jsonschema` package (install via `pip install jsonschema`).