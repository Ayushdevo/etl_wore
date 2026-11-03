"""Decode HTML character references once; this operation does not sanitize HTML."""

import html
from ._records import FieldTransform


class UnescapeHtml(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return html.unescape(value)
