"""Split string fields on a literal separator, preserving empty components."""

from ._records import FieldTransform


class SplitText(FieldTransform):
    def __init__(self, fields, separator, maxsplit=None):
        super().__init__(fields)
        if not isinstance(separator, str) or not separator:
            raise ValueError("separator must be a nonempty string")
        if maxsplit is not None and (
            isinstance(maxsplit, bool) or not isinstance(maxsplit, int) or maxsplit < 0
        ):
            raise ValueError("maxsplit must be a nonnegative integer or None")
        self.separator, self.maxsplit = separator, maxsplit

    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return value.split(
            self.separator, -1 if self.maxsplit is None else self.maxsplit
        )
