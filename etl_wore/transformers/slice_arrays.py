"""Slice arrays using Python start, stop and nonzero step semantics, preserving input order."""

from ._records import FieldTransform


class SliceArrays(FieldTransform):
    def __init__(self, fields, start=None, stop=None, step=1):
        super().__init__(fields)
        for name, value in (("start", start), ("stop", stop), ("step", step)):
            if value is None and name != "step":
                continue
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
        if step == 0:
            raise ValueError("step must be nonzero")
        self.slice = slice(start, stop, step)

    def convert(self, value):
        if not isinstance(value, list):
            raise ValueError("expected an array")
        return value[self.slice]
