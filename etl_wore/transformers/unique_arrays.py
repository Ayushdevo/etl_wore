"""Deduplicate strict JSON array values in first-seen order; distinguish booleans from numbers."""

import json
from ..loaders.json_loader import _validate_keys
from ._records import FieldTransform


class UniqueArrays(FieldTransform):
    def convert(self, value):
        if not isinstance(value, list):
            raise ValueError("expected an array")
        _validate_keys(value)
        seen, result = set(), []
        for item in value:
            key = json.dumps(
                item, sort_keys=True, allow_nan=False, separators=(",", ":")
            )
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result
