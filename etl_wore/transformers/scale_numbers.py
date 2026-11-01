"""Apply a finite factor and offset, rejecting nonnumeric inputs and overflow."""

from ._records import FieldTransform, finite_number


class ScaleNumbers(FieldTransform):
    def __init__(self, fields, factor=1, offset=0):
        super().__init__(fields)
        self.factor = finite_number(factor)
        self.offset = finite_number(offset)

    def convert(self, value):
        value = finite_number(value)
        return finite_number(value * self.factor + self.offset)
