"""Project ordered fields; optionally require every selected field."""

from ..exceptions import TransformationError
from ._records import boolean, field_names, record_copy
from .base import BaseTransformer


class SelectFields(BaseTransformer):
    def __init__(self, fields, require_all=False):
        super().__init__()
        self.fields = field_names(fields)
        self.require_all = boolean(require_all, "require_all")

    def transform(self, record):
        out = record_copy(record)
        if self.require_all and any(field not in out for field in self.fields):
            raise TransformationError("Selected field is missing")
        return {field: out[field] for field in self.fields if field in out}
