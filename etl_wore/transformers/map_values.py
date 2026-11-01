"""Map string categories to copied values; optionally reject unmapped values."""

from copy import deepcopy

from ..exceptions import TransformationError
from ._records import (
    boolean,
    field_name,
    record_copy,
)
from .base import BaseTransformer


class MapValues(BaseTransformer):
    def __init__(self, field, mapping, strict=False):
        super().__init__()
        self.field = field_name(field)
        if (
            not isinstance(mapping, dict)
            or not mapping
            or any(not isinstance(key, str) for key in mapping)
        ):
            raise ValueError("mapping must be a nonempty object with string keys")
        self.mapping = deepcopy(mapping)
        self.strict = boolean(strict, "strict")

    def transform(self, record):
        out = record_copy(record)
        if self.field not in out:
            return out
        value = out[self.field]
        if isinstance(value, str) and value in self.mapping:
            out[self.field] = deepcopy(self.mapping[value])
        elif self.strict:
            raise TransformationError(f"Unmapped value in field {self.field!r}")
        return out
