"""Keep or exclude records matching one field value; distinguish missing, null, and booleans."""

from copy import deepcopy

from ._records import (
    boolean,
    field_name,
    record_copy,
)
from .base import BaseTransformer


class FilterValue(BaseTransformer):
    def __init__(self, field, value, exclude=False):
        super().__init__()
        self.field = field_name(field)
        self.value = deepcopy(value)
        self.exclude = boolean(exclude, "exclude")

    def transform(self, record):
        out = record_copy(record)
        matches = (
            self.field in out
            and type(out[self.field]) is type(self.value)
            and out[self.field] == self.value
        )
        return out if matches != self.exclude else None
