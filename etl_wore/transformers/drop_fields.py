"""Remove selected fields, ignoring absent names."""

from ._records import field_names, record_copy
from .base import BaseTransformer


class DropFields(BaseTransformer):
    def __init__(self, fields):
        super().__init__()
        self.fields = field_names(fields)

    def transform(self, record):
        out = record_copy(record)
        for field in self.fields:
            out.pop(field, None)
        return out
