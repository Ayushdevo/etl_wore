"""Attach constant fields such as source provenance, with optional overwrite protection."""

from copy import deepcopy

from ..exceptions import TransformationError
from ._records import (
    boolean,
    field_name,
    record_copy,
)
from .base import BaseTransformer


class ConstantFields(BaseTransformer):
    def __init__(self, values, overwrite=True):
        super().__init__()
        if not isinstance(values, dict) or not values:
            raise ValueError("values must be a nonempty field mapping")
        for key in values:
            field_name(key)
        self.values = deepcopy(values)
        self.overwrite = boolean(overwrite, "overwrite")

    def transform(self, record):
        out = record_copy(record)
        if not self.overwrite and set(out).intersection(self.values):
            raise TransformationError("Constant would overwrite an existing field")
        out.update(deepcopy(self.values))
        return out
