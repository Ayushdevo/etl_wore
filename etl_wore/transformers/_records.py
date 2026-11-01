"""Validation and copy-on-transform utilities for built-in record operations."""

import math
from copy import deepcopy

from ..exceptions import TransformationError
from .base import BaseTransformer


def field_name(value):
    if not isinstance(value, str) or not value:
        raise ValueError("field names must be nonempty strings")
    return value


def field_names(value):
    if not isinstance(value, (list, tuple)) or not value:
        raise ValueError("fields must be a nonempty sequence")
    fields = tuple(field_name(item) for item in value)
    if len(set(fields)) != len(fields):
        raise ValueError("field names must be unique")
    return fields


def field_mapping(value):
    if not isinstance(value, dict) or not value:
        raise ValueError("mapping must be a nonempty object")
    return {field_name(key): field_name(item) for key, item in value.items()}


def boolean(value, name):
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean")
    return value


def finite_number(value):
    try:
        valid = (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError("expected a finite number")
    return value


def record_copy(record):
    if not isinstance(record, dict):
        raise TransformationError("Record must be an object")
    return deepcopy(record)


class FieldTransform(BaseTransformer):
    """Preserve missing/null fields and reject incompatible non-null values."""

    skip_null = True

    def __init__(self, fields):
        super().__init__()
        self.fields = field_names(fields)

    def transform(self, record):
        out = record_copy(record)
        for field in self.fields:
            if field not in out or (out[field] is None and self.skip_null):
                continue
            try:
                out[field] = self.convert(out[field])
            except (TypeError, ValueError, OverflowError) as exc:
                raise TransformationError(f"Field {field!r}: {exc}") from exc
        return out

    def convert(self, value):
        raise NotImplementedError
