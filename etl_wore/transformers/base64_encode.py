"""Encode UTF-8 text with standard padded Base64."""

import base64
from ._records import FieldTransform


class Base64Encode(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return base64.b64encode(value.encode("utf-8")).decode("ascii")
