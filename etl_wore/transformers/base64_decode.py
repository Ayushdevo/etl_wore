"""Decode canonical standard Base64 to UTF-8 text; reject malformed or binary payloads."""

import base64
from ._records import FieldTransform


class Base64Decode(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        decoded = base64.b64decode(value, validate=True)
        if base64.b64encode(decoded).decode("ascii") != value:
            raise ValueError("expected canonical padded Base64")
        return decoded.decode("utf-8")
