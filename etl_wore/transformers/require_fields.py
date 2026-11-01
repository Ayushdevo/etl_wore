"""Require selected fields with explicit null and drop policies."""

from ..exceptions import TransformationError
from ._records import boolean, field_names, record_copy
from .base import BaseTransformer


class RequireFields(BaseTransformer):
    def __init__(self, fields, drop_invalid=False, allow_null=False):
        super().__init__()
        self.fields = field_names(fields)
        self.drop_invalid = boolean(drop_invalid, "drop_invalid")
        self.allow_null = boolean(allow_null, "allow_null")

    def transform(self, record):
        out = record_copy(record)
        missing = [
            field
            for field in self.fields
            if field not in out or (out[field] is None and not self.allow_null)
        ]
        if missing:
            if self.drop_invalid:
                return None
            raise TransformationError(f"Required fields missing or null: {missing}")
        return out
