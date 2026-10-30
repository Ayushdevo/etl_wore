"""Construct pipelines from a closed, validated set of built-in components."""
import codecs
from copy import deepcopy
from urllib.parse import urlparse

from .extractors.csv_extractor import CsvExtractor
from .exceptions import ConfigurationError
from .pipeline.engine import Pipeline


def _string(value):
    return isinstance(value, str) and bool(value.strip())


def _boolean(value):
    return isinstance(value, bool)


def _positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


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
    return isinstance(value, dict) and all(_string(key) and isinstance(item, str) for key, item in value.items())


def _http_url(value):
    if not _string(value):
        return False
    try:
        parts = urlparse(value)
        return parts.scheme in {"http", "https"} and bool(parts.hostname)
    except ValueError:
        return False


# Entries are (constructor, required options, option validators). No dynamic imports.
_EXTRACTORS = {
    "csv": (CsvExtractor, ['filepath'], {"filepath": _string, "delimiter": _delimiter, "encoding": _encoding}),}
_TRANSFORMERS = {}
_LOADERS = {}


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
                raise ConfigurationError(f"{section}[{index}] must be a mapping with a nonempty type")


def _component(entry, registry, location):
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
        if not validators[name](value):
            raise ConfigurationError(f"{location}: invalid option {name}")
    try:
        return constructor(**options)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{location}: {exc}") from exc


def build_pipeline(spec):
    """Build built-in components; no input, output, or network I/O is performed."""
    validate_spec(spec)
    pipeline = Pipeline(spec["name"], batch_size=spec.get("batch_size", 500))
    for section, registry, add in (
        ("extractors", _EXTRACTORS, pipeline.add_extractor),
        ("transformers", _TRANSFORMERS, pipeline.add_transformer),
        ("loaders", _LOADERS, pipeline.add_loader),
    ):
        for index, entry in enumerate(spec.get(section, [])):
            add(_component(entry, registry, f"{section}[{index}]"))
    return pipeline
