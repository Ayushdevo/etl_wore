"""Parse true/false and 1/0 text or integer flags explicitly; preserve existing booleans."""

from ._records import FieldTransform


class ParseBooleans(FieldTransform):
    def convert(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, int) and value in (0, 1):
            return bool(value)
        if isinstance(value, str):
            token = value.strip().casefold()
            if token in {"true", "1"}:
                return True
            if token in {"false", "0"}:
                return False
        raise ValueError("expected true, false, 1 or 0")
