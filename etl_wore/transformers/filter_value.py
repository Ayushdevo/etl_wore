"""Keep or exclude records matching one field value; distinguish missing, null, and booleans."""

from copy import deepcopy

from ._records import (
    boolean,
    field_name,
    record_copy,
)
from .base import BaseTransformer


def _equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_equal(left[key], right[key]) for key in left)
    if isinstance(left, (list, tuple)):
        return len(left) == len(right) and all(_equal(a, b) for a, b in zip(left, right))
    return left == right


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
            and _equal(out[self.field], self.value)
        )
        return out if matches != self.exclude else None
