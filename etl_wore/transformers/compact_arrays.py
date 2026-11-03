"""Remove only null array elements, preserving zero, false and empty strings."""

from ._records import FieldTransform


class CompactArrays(FieldTransform):
    def convert(self, value):
        if not isinstance(value, list):
            raise ValueError("expected an array")
        return [item for item in value if item is not None]
