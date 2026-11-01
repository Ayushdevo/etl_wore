"""Fill absent fields with independent default values; optionally replace nulls."""

from copy import deepcopy

from ._records import (
    boolean,
    field_name,
    record_copy,
)
from .base import BaseTransformer


class DefaultFields(BaseTransformer):
    def __init__(self, values, replace_null=False):
        super().__init__()
        if not isinstance(values, dict) or not values:
            raise ValueError("values must be a nonempty field mapping")
        for key in values:
            field_name(key)
        self.values = deepcopy(values)
        self.replace_null = boolean(replace_null, "replace_null")

    def transform(self, record):
        out = record_copy(record)
        for field, value in self.values.items():
            if field not in out or (self.replace_null and out[field] is None):
                out[field] = deepcopy(value)
        return out
