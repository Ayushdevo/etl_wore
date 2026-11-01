"""Normalize string case using lower, upper, Unicode casefold, or title."""

from ._records import FieldTransform


class StringCase(FieldTransform):
    def __init__(self, fields, mode="casefold"):
        super().__init__(fields)
        if mode not in ("lower", "upper", "casefold", "title"):
            raise ValueError("mode must be lower, upper, casefold or title")
        self.mode = mode

    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return getattr(value, self.mode)()
