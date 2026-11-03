"""Extract the first regular-expression match or chosen group; unmatched fields become null."""

import re
from ._records import FieldTransform


class RegexExtract(FieldTransform):
    def __init__(self, fields, pattern, group=0):
        super().__init__(fields)
        if not isinstance(pattern, str):
            raise ValueError("pattern must be a string")
        try:
            self.pattern = re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"invalid regular expression: {exc}") from exc
        if isinstance(group, bool) or not isinstance(group, (str, int)):
            raise ValueError("group must be an integer or a named group")
        if isinstance(group, int):
            if group < 0 or group > self.pattern.groups:
                raise ValueError("group index is out of range")
        elif group not in self.pattern.groupindex:
            raise ValueError("unknown named group")
        self.group = group

    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError("expected a string")
        match = self.pattern.search(value)
        return None if match is None else match.group(self.group)
