"""Flatten nested objects to separated paths, preserving arrays and empty objects; reject ambiguous keys."""

from copy import deepcopy

from ..exceptions import TransformationError
from ._records import (
    field_name,
    record_copy,
)
from .base import BaseTransformer


class FlattenRecord(BaseTransformer):
    def __init__(self, separator="."):
        super().__init__()
        self.separator = field_name(separator)

    def transform(self, record):
        record_copy(record)  # Validate input before traversal.
        result, active = {}, set()

        def visit(mapping, prefix):
            if id(mapping) in active:
                raise TransformationError("Cannot flatten a cyclic object")
            active.add(id(mapping))
            try:
                for key, value in mapping.items():
                    if not isinstance(key, str) or not key or self.separator in key:
                        raise TransformationError(
                            "Flatten keys must be nonempty strings without the separator"
                        )
                    path = prefix + self.separator + key if prefix else key
                    expected_parts = (
                        prefix.split(self.separator) + [key] if prefix else [key]
                    )
                    if path.split(self.separator) != expected_parts:
                        raise TransformationError(
                            "Flatten separator creates an ambiguous path"
                        )
                    if isinstance(value, dict) and value:
                        visit(value, path)
                    else:
                        result[path] = deepcopy(value)
            finally:
                active.remove(id(mapping))

        visit(record, "")
        return result
