"""
Schema validation and field type casting.
"""
import math
from typing import Dict, Any, Optional, Type
from .base import BaseTransformer
from ..exceptions import TransformationError

class SchemaValidator(BaseTransformer):
    def __init__(self, schema: Dict[str, Type], drop_invalid: bool = False):
        super().__init__()
        if not isinstance(schema, dict) or any(
            not isinstance(key, str) or not key or kind not in (str, int, float, bool)
            for key, kind in schema.items()
        ):
            raise ValueError("schema must map nonempty field names to str, int, float or bool")
        if not isinstance(drop_invalid, bool):
            raise ValueError("drop_invalid must be a boolean")
        self.schema = dict(schema)
        self.drop_invalid = drop_invalid

    def transform(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        transformed = dict(record)
        for field, expected_type in self.schema.items():
            if field not in transformed:
                if self.drop_invalid:
                    return None
                raise TransformationError(f"Missing required field: {field}")

            val = transformed[field]
            if not isinstance(val, expected_type) or (isinstance(val, bool) and expected_type is int):
                try:
                    if expected_type is bool:
                        normalized = str(val).strip().casefold()
                        if normalized not in {"true", "false", "1", "0"}:
                            raise ValueError("Expected true, false, 1, or 0")
                        transformed[field] = normalized in {"true", "1"}
                    else:
                        if expected_type is int and isinstance(val, float) and math.isfinite(val) and not val.is_integer():
                            raise ValueError('Cannot cast a fractional value to int without data loss')
                        converted = expected_type(val)
                        if expected_type is int and not isinstance(val, (str, bytes, bytearray, bool)) and converted != val:
                            raise ValueError("Cannot cast a fractional value to int without data loss")
                        transformed[field] = converted
                except (ValueError, TypeError, OverflowError) as e:
                    if self.drop_invalid:
                        return None
                    raise TransformationError(f"Field '{field}' could not be cast to {expected_type}: {e}")
            if expected_type is float and not math.isfinite(transformed[field]):
                if self.drop_invalid:
                    return None
                raise TransformationError(f"Field '{field}' must be finite")
        return transformed

