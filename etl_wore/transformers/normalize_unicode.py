"""Normalize text with NFC by default; support NFD, NFKC and NFKD explicitly."""

import unicodedata
from ._records import FieldTransform


class NormalizeUnicode(FieldTransform):
    def __init__(self, fields, form="NFC"):
        super().__init__(fields)
        if not isinstance(form, str) or form not in {"NFC", "NFD", "NFKC", "NFKD"}:
            raise ValueError("form must be NFC, NFD, NFKC or NFKD")
        self.form = form

    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return unicodedata.normalize(self.form, value)
