"""Percent-encode a complete UTF-8 URL component, including slashes and spaces."""

from urllib.parse import quote
from ._records import FieldTransform


class UrlEncode(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return quote(value, safe="", encoding="utf-8", errors="strict")
