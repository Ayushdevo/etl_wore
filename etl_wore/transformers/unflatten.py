"""Rebuild nested objects from separated paths; reject prefix collisions in either input order."""

from ..exceptions import TransformationError
from ._records import field_name, record_copy
from .base import BaseTransformer


class UnflattenRecord(BaseTransformer):
    def __init__(self, separator="."):
        super().__init__()
        self.separator = field_name(separator)

    def transform(self, record):
        out = record_copy(record)
        result, leaves = {}, set()
        for key, value in out.items():
            if not isinstance(key, str):
                raise TransformationError("Unflatten keys must be strings")
            parts = key.split(self.separator)
            if any(not part for part in parts):
                raise TransformationError(
                    "Unflatten paths must not have empty components"
                )
            current = result
            prefix = []
            for part in parts[:-1]:
                prefix.append(part)
                if tuple(prefix) in leaves:
                    raise TransformationError("Conflicting unflatten paths")
                current = current.setdefault(part, {})
            if parts[-1] in current:
                raise TransformationError("Conflicting unflatten paths")
            current[parts[-1]] = value
            leaves.add(tuple(parts))
        return result
