"""Replace regular-expression matches; validate patterns and backreferences during dry run."""

import re

from ._records import FieldTransform


class RegexReplace(FieldTransform):
    def __init__(self, fields, pattern, replacement, count=0):
        super().__init__(fields)
        if not isinstance(pattern, str) or not isinstance(replacement, str):
            raise ValueError("pattern and replacement must be strings")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError("count must be a nonnegative integer")
        try:
            self.pattern = re.compile(pattern)
            self.pattern.sub(
                replacement, ""
            )  # Validate replacement backreferences now.
        except re.error as exc:
            raise ValueError(f"Invalid regular expression: {exc}") from exc
        self.replacement, self.count = replacement, count

    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        return self.pattern.sub(self.replacement, value, count=self.count)
