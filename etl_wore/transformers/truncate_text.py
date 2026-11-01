"""Limit string length by Unicode code points; permit zero-length output."""

from ._records import FieldTransform


class TruncateText(FieldTransform):
    def __init__(self, fields, max_length):
        super().__init__(fields)
        if (
            isinstance(max_length, bool)
            or not isinstance(max_length, int)
            or max_length < 0
        ):
            raise ValueError("max_length must be a nonnegative integer")
        self.max_length = max_length

    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return value[: self.max_length]
