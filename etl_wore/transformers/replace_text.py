"""Replace literal text with an optional nonnegative replacement limit."""

from ._records import FieldTransform


class ReplaceText(FieldTransform):
    def __init__(self, fields, old, new, count=None):
        super().__init__(fields)
        if not isinstance(old, str) or not old or not isinstance(new, str):
            raise ValueError("old must be a nonempty string and new a string")
        if count is not None and (
            isinstance(count, bool) or not isinstance(count, int) or count < 0
        ):
            raise ValueError("count must be a nonnegative integer or None")
        self.old, self.new, self.count = old, new, count

    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return value.replace(
            self.old, self.new, -1 if self.count is None else self.count
        )
