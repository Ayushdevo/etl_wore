"""
Schema validation and field type casting.
"""
from typing import Dict, Any, Optional, Type
from .base import BaseTransformer
from ..exceptions import TransformationError

class SchemaValidator(BaseTransformer):
    def __init__(self, schema: Dict[str, Type], drop_invalid: bool = False):
        super().__init__()
        self.schema = schema
        self.drop_invalid = drop_invalid

    def transform(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        transformed = dict(record)
        for field, expected_type in self.schema.items():
            if field not in transformed:
                if self.drop_invalid:
                    return None
                raise TransformationError(f"Missing required field: {field}")

            val = transformed[field]
            if not isinstance(val, expected_type):
                try:
                    transformed[field] = expected_type(val)
                except (ValueError, TypeError) as e:
                    if self.drop_invalid:
                        return None
                    raise TransformationError(f"Field '{field}' could not be cast to {expected_type}: {e}")
        return transformed
