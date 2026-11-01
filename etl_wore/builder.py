"""Construct pipelines from a closed, validated set of built-in components."""

import codecs
import math
import os
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlparse

from .exceptions import ConfigurationError
from .extractors.api_extractor import RestApiExtractor
from .extractors.csv_extractor import CsvExtractor
from .extractors.json_extractor import JsonExtractor
from .loaders.csv_loader import CsvLoader
from .loaders.json_loader import JsonLinesLoader
from .loaders.sqlite_loader import SqliteLoader, _identifier_key
from .pipeline.engine import Pipeline
from .transformers.select_fields import SelectFields
from .transformers.drop_fields import DropFields
from .transformers.rename_fields import RenameFields
from .transformers.copy_fields import CopyFields
from .transformers.defaults import DefaultFields
from .transformers.constants import ConstantFields
from .transformers.coalesce import CoalesceFields
from .transformers.date_normalizer import DateNormalizer
from .transformers.deduplicator import DeduplicationTransformer
from .transformers.sanitizer import DataSanitizer
from .transformers.schema_validator import SchemaValidator


def _string(value):
    return isinstance(value, str) and bool(value.strip())


def _boolean(value):
    return isinstance(value, bool)


def _positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _positive_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value > 0
    )


def _strings(value):
    return isinstance(value, list) and all(_string(item) for item in value)


def _delimiter(value):
    return isinstance(value, str) and len(value) == 1 and value not in "\r\n\0"


def _encoding(value):
    if not _string(value):
        return False
    try:
        codecs.lookup(value)
        return True
    except LookupError:
        return False


def _headers(value):
    return isinstance(value, dict) and all(
        _string(key) and isinstance(item, str) for key, item in value.items()
    )


def _http_url(value):
    if not _string(value):
        return False
    try:
        parts = urlparse(value)
        return parts.scheme in {"http", "https"} and bool(parts.hostname)
    except ValueError:
        return False


_SCHEMA_TYPES = {"str": str, "int": int, "float": float, "bool": bool}


def _schema(value):
    return (
        isinstance(value, dict)
        and bool(value)
        and all(
            _string(key) and isinstance(kind, str) and kind in _SCHEMA_TYPES
            for key, kind in value.items()
        )
    )


def _schema_validator(schema, drop_invalid=False):
    return SchemaValidator(
        {key: _SCHEMA_TYPES[kind] for key, kind in schema.items()}, drop_invalid=drop_invalid
    )


# Entries are (constructor, required options, option validators). No dynamic imports.
_EXTRACTORS = {
    "rest": (
        RestApiExtractor,
        ["endpoint"],
        {
            "endpoint": _http_url,
            "headers": _headers,
            "page_param": _string,
            "max_pages": _positive_int,
            "timeout": _positive_number,
        },
    ),
    "json": (
        JsonExtractor,
        ["filepath"],
        {"filepath": _string, "is_lines": _boolean, "encoding": _encoding},
    ),
    "csv": (
        CsvExtractor,
        ["filepath"],
        {"filepath": _string, "delimiter": _delimiter, "encoding": _encoding},
    ),
}
_TRANSFORMERS = {
    'coalesce': (CoalesceFields, ['fields', 'target'], {'fields': lambda value: True, 'target': lambda value: True, 'skip_empty': lambda value: True}),
    'constants': (ConstantFields, ['values'], {'values': lambda value: True, 'overwrite': lambda value: True}),
    'defaults': (DefaultFields, ['values'], {'values': lambda value: True, 'replace_null': lambda value: True}),
    'copy_fields': (CopyFields, ['mapping'], {'mapping': lambda value: True, 'overwrite': lambda value: True}),
    'rename_fields': (RenameFields, ['mapping'], {'mapping': lambda value: True}),
    'drop_fields': (DropFields, ['fields'], {'fields': lambda value: True}),
    'select_fields': (SelectFields, ['fields'], {'fields': lambda value: True, 'require_all': lambda value: True}),
    "dates": (
        DateNormalizer,
        ["date_fields"],
        {"date_fields": lambda value: _strings(value) and bool(value), "output_format": _string},
    ),
    "deduplicate": (
        DeduplicationTransformer,
        ["key_fields"],
        {"key_fields": lambda value: _strings(value) and bool(value)},
    ),
    "schema": (_schema_validator, ["schema"], {"schema": _schema, "drop_invalid": _boolean}),
    "sanitize": (DataSanitizer, [], {"strip_strings": _boolean, "mask_fields": _strings}),
}
_LOADERS = {
    "sqlite": (
        SqliteLoader,
        ["db_path", "table_name"],
        {"db_path": _string, "table_name": _string},
    ),
    "jsonl": (JsonLinesLoader, ["output_path"], {"output_path": _string}),
    "csv": (CsvLoader, ["output_path"], {"output_path": _string, "delimiter": _delimiter}),
}


def validate_spec(spec):
    """Validate the pipeline envelope without opening sources or destinations."""
    if not isinstance(spec, dict):
        raise ConfigurationError("Pipeline specification must be a mapping")
    unknown = set(spec) - {"name", "batch_size", "extractors", "transformers", "loaders"}
    if unknown:
        raise ConfigurationError(f"Unknown pipeline options: {sorted(map(str, unknown))}")
    if not _string(spec.get("name")):
        raise ConfigurationError("name must be a nonempty string")
    if not _positive_int(spec.get("batch_size", 500)):
        raise ConfigurationError("batch_size must be a positive integer")
    for section in ("extractors", "transformers", "loaders"):
        entries = spec.get(section, [])
        if not isinstance(entries, list):
            raise ConfigurationError(f"{section} must be a list")
        if section != "transformers" and not entries:
            raise ConfigurationError(f"{section} must contain at least one component")
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict) or not _string(entry.get("type")):
                raise ConfigurationError(
                    f"{section}[{index}] must be a mapping with a nonempty type"
                )


def _component(entry, registry, location, base_dir=None):
    kind = entry["type"]
    if kind not in registry:
        raise ConfigurationError(f"{location}: unsupported component type {kind!r}")
    constructor, required, validators = registry[kind]
    options = {key: deepcopy(value) for key, value in entry.items() if key != "type"}
    unknown = set(options) - set(validators)
    if unknown:
        raise ConfigurationError(f"{location}: unknown options {sorted(map(str, unknown))}")
    for name in required:
        if name not in options:
            raise ConfigurationError(f"{location}: missing required option {name}")
    for name, value in options.items():
        try:
            valid = validators[name](value)
        except (TypeError, ValueError, OverflowError):
            valid = False
        if not valid:
            raise ConfigurationError(f"{location}: invalid option {name}")
    if base_dir is not None:
        for name in ("filepath", "output_path", "db_path"):
            if name in options:
                try:
                    options[name] = str((Path(base_dir) / options[name]).resolve())
                except (OSError, ValueError, RuntimeError) as exc:
                    raise ConfigurationError(f"{location}: invalid {name}: {exc}") from exc
    try:
        return constructor(**options)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{location}: {exc}") from exc


def _same_path(left, right):
    try:
        if Path(left).resolve() == Path(right).resolve():
            return True
    except (OSError, ValueError, RuntimeError) as exc:
        raise ConfigurationError(f"Invalid file path: {exc}") from exc
    try:
        return os.path.samefile(left, right)
    except OSError:
        return False


def _validate_destinations(pipeline):
    sources = [source.filepath for source in pipeline.extractors if hasattr(source, "filepath")]
    destinations = []
    for sink in pipeline.loaders:
        target = getattr(sink, "output_path", getattr(sink, "db_path", None))
        if any(_same_path(source, target) for source in sources):
            raise ConfigurationError("An output destination must not overwrite an input source")
        for previous in destinations:
            previous_target = getattr(previous, "output_path", getattr(previous, "db_path", None))
            if _same_path(target, previous_target):
                distinct_tables = (
                    isinstance(sink, SqliteLoader)
                    and isinstance(previous, SqliteLoader)
                    and _identifier_key(sink.table_name) != _identifier_key(previous.table_name)
                )
                if not distinct_tables:
                    raise ConfigurationError("Output destinations must be distinct")
        destinations.append(sink)


def build_pipeline(spec, base_dir=None):
    """Build components without reading records, writing outputs or making network requests."""
    validate_spec(spec)
    base_dir = Path.cwd() if base_dir is None else Path(base_dir)
    pipeline = Pipeline(spec["name"], batch_size=spec.get("batch_size", 500))
    for section, registry, add in (
        ("extractors", _EXTRACTORS, pipeline.add_extractor),
        ("transformers", _TRANSFORMERS, pipeline.add_transformer),
        ("loaders", _LOADERS, pipeline.add_loader),
    ):
        for index, entry in enumerate(spec.get(section, [])):
            add(_component(entry, registry, f"{section}[{index}]", base_dir=base_dir))
    _validate_destinations(pipeline)
    return pipeline
