"""Strip leading and trailing Unicode whitespace from selected text fields."""

from ._records import FieldTransform


class StripText(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return value.strip()
