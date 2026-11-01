"""Encode values as compact UTF-8 JSON; reject nonfinite numbers and nonstring object keys."""

import json

from ..loaders.json_loader import _validate_keys
from ._records import FieldTransform, boolean


class EncodeJsonFields(FieldTransform):
    skip_null = False

    def __init__(self, fields, sort_keys=True):
        super().__init__(fields)
        self.sort_keys = boolean(sort_keys, "sort_keys")

    def convert(self, value):
        _validate_keys(value)
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=self.sort_keys,
            separators=(",", ":"),
        )
