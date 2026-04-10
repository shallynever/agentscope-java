import json
from jsonschema import validate, ValidationError


class JSONValidator:
    def validate(self, json_string: str, schema: dict = None) -> dict:
        """Validate JSON string for syntax and optional schema compliance"""
        try:
            # Check basic JSON syntax
            data = json.loads(json_string)
            
            # Schema validation (if provided)
            if schema:
                validate(instance=data, schema=schema)
                
            return {"valid": True}
        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "error": f"Syntax error at line {e.lineno} column {e.colno}: {e.msg}"
            }
        except ValidationError as e:
            return {
                "valid": False,
                "error": f"Schema violation: {e.message}"
            }


# Example usage:
# validator = JSONValidator()
# result = validator.validate('{"name": "test"}', schema={"type": "object"})