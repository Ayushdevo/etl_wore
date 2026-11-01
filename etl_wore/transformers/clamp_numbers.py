"""Clip finite numbers to one or two validated bounds."""

from ._records import FieldTransform, finite_number


class ClampNumbers(FieldTransform):
    def __init__(self, fields, minimum=None, maximum=None):
        super().__init__(fields)
        if minimum is None and maximum is None:
            raise ValueError("at least one bound is required")
        self.minimum = None if minimum is None else finite_number(minimum)
        self.maximum = None if maximum is None else finite_number(maximum)
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("minimum must not exceed maximum")

    def convert(self, value):
        value = finite_number(value)
        if self.minimum is not None:
            value = max(value, self.minimum)
        if self.maximum is not None:
            value = min(value, self.maximum)
        return value
