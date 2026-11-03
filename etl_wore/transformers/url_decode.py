"""Decode percent-encoded UTF-8 components strictly; preserve literal plus signs."""

import re
from urllib.parse import unquote
from ._records import FieldTransform


class UrlDecode(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        if re.search(r"%(?![0-9A-Fa-f]{2})", value):
            raise ValueError("invalid percent escape")
        return unquote(value, encoding="utf-8", errors="strict")
