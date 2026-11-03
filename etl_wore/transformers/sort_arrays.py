"""Sort homogeneous string or finite numeric arrays, optionally in descending order."""

from ._records import boolean, finite_number
from ._records import FieldTransform


class SortArrays(FieldTransform):
    def __init__(self, fields, descending=False):
        super().__init__(fields)
        self.descending = boolean(descending, "descending")

    def convert(self, value):
        if not isinstance(value, list):
            raise ValueError("expected an array")
        if not all(isinstance(item, str) for item in value):
            for item in value:
                finite_number(item)
        return sorted(value, reverse=self.descending)
