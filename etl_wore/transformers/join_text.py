"""Join arrays of strings without silently coercing numbers or scalar strings."""

from ._records import FieldTransform


class JoinText(FieldTransform):
    def __init__(self, fields, separator=","):
        super().__init__(fields)
        if not isinstance(separator, str):
            raise ValueError("separator must be a string")
        self.separator = separator

    def convert(self, value):
        if not isinstance(value, (list, tuple)) or any(
            not isinstance(item, str) for item in value
        ):
            raise ValueError("expected an array of strings")
        return self.separator.join(value)
