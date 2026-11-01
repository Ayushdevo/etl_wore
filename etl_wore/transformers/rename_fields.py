"""Rename fields simultaneously, support swaps, and reject overwrites."""

from ..exceptions import TransformationError
from ._records import field_mapping, record_copy
from .base import BaseTransformer


class RenameFields(BaseTransformer):
    def __init__(self, mapping):
        super().__init__()
        self.mapping = field_mapping(mapping)
        if len(set(self.mapping.values())) != len(self.mapping):
            raise ValueError("Rename destinations must be unique")

    def transform(self, record):
        out = record_copy(record)
        active = {
            source: target for source, target in self.mapping.items() if source in out
        }
        if any(target in out and target not in active for target in active.values()):
            raise TransformationError("Rename would overwrite an existing field")
        values = {target: out[source] for source, target in active.items()}
        for source in active:
            del out[source]
        out.update(values)
        return out
