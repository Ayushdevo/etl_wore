"""Choose the first present non-null input field, preserving zero and false."""

from copy import deepcopy

from ._records import (
    boolean,
    field_name,
    field_names,
    record_copy,
)
from .base import BaseTransformer


class CoalesceFields(BaseTransformer):
    def __init__(self, fields, target, skip_empty=False):
        super().__init__()
        self.fields = field_names(fields)
        self.target = field_name(target)
        self.skip_empty = boolean(skip_empty, "skip_empty")

    def transform(self, record):
        out = record_copy(record)
        for field in self.fields:
            if (
                field in out
                and out[field] is not None
                and not (self.skip_empty and out[field] == "")
            ):
                out[self.target] = deepcopy(out[field])
                break
        return out
