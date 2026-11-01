"""Copy original field values to new destinations; reject overwrites by default."""

from copy import deepcopy

from ..exceptions import TransformationError
from ._records import (
    boolean,
    field_mapping,
    record_copy,
)
from .base import BaseTransformer


class CopyFields(BaseTransformer):
    def __init__(self, mapping, overwrite=False):
        super().__init__()
        self.mapping = field_mapping(mapping)
        self.overwrite = boolean(overwrite, "overwrite")
        if len(set(self.mapping.values())) != len(self.mapping):
            raise ValueError("Copy destinations must be unique")

    def transform(self, record):
        out = record_copy(record)
        active = {
            source: target
            for source, target in self.mapping.items()
            if source in record
        }
        if not self.overwrite and any(target in out for target in active.values()):
            raise TransformationError("Copy would overwrite an existing field")
        out.update(
            {target: deepcopy(record[source]) for source, target in active.items()}
        )
        return out
