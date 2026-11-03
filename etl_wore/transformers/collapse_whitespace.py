"""Replace runs of Unicode whitespace with single spaces and trim their edges."""

from ._records import FieldTransform


class CollapseWhitespace(FieldTransform):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return " ".join(value.split())
