"""Round finite numbers using Python ties-to-even semantics and integer precision."""

from ._records import FieldTransform, finite_number


class RoundNumbers(FieldTransform):
    def __init__(self, fields, digits=0):
        super().__init__(fields)
        if isinstance(digits, bool) or not isinstance(digits, int):
            raise ValueError("digits must be an integer")
        self.digits = digits

    def convert(self, value):
        return finite_number(round(finite_number(value), self.digits))
