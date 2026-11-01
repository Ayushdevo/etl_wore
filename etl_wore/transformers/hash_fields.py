"""Compute stable field digests from strict canonical JSON; hashing alone does not anonymize personal data."""

import hashlib
import json

from ..exceptions import TransformationError
from ..loaders.json_loader import _validate_keys
from ._records import field_name, field_names, record_copy
from .base import BaseTransformer


class HashFields(BaseTransformer):
    def __init__(self, fields, target, algorithm="sha256"):
        super().__init__()
        self.fields = field_names(fields)
        self.target = field_name(target)
        if algorithm not in ("sha256", "sha512", "blake2b"):
            raise ValueError("algorithm must be sha256, sha512 or blake2b")
        self.algorithm = algorithm

    def transform(self, record):
        out = record_copy(record)
        if any(field not in out for field in self.fields):
            raise TransformationError("Cannot hash missing fields")
        try:
            payload = {field: out[field] for field in self.fields}
            _validate_keys(payload)
            encoded = json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
            out[self.target] = hashlib.new(self.algorithm, encoded).hexdigest()
        except (TypeError, ValueError, UnicodeError) as exc:
            raise TransformationError(f"Cannot hash fields: {exc}") from exc
        return out
