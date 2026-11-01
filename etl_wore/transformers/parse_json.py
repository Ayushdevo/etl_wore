"""Parse embedded JSON while rejecting duplicate keys and nonfinite numbers."""

import json

from ..extractors.json_extractor import _finite_float, _reject_constant, _unique_object
from ._records import FieldTransform


class ParseJsonFields(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a JSON string")
        return json.loads(
            value,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
            object_pairs_hook=_unique_object,
        )
