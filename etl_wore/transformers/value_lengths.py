"""Replace text, array or object fields with their lengths; text length counts Unicode code points."""

from ._records import FieldTransform


class ValueLengths(FieldTransform):
    def convert(self, value):
        if not isinstance(value, (str, list, dict)):
            raise ValueError("expected text, an array or an object")
        return len(value)
