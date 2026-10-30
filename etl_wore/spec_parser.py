"""Declarative JSON/YAML pipeline specification parser."""

import json
import math
import os
from typing import Any, Dict

from .exceptions import ConfigurationError


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str):
            raise ConfigurationError("Specification mapping keys must be strings")
        if key in result:
            raise ConfigurationError(f"Duplicate specification key: {key}")
        result[key] = value
    return result


def _finite_float(text):
    value = float(text)
    if not math.isfinite(value):
        raise ConfigurationError(f"Non-finite specification number: {text}")
    return value


def _reject_constant(text):
    raise ConfigurationError(f"Invalid JSON constant in specification: {text}")


class SpecParser:
    @staticmethod
    def parse_file(filepath: str) -> Dict[str, Any]:
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in {".json", ".yaml", ".yml"}:
            raise ConfigurationError(f"Unsupported spec format: {ext}")
        try:
            with open(filepath, "r", encoding="utf-8-sig") as source:
                if ext == ".json":
                    spec = json.load(
                        source,
                        object_pairs_hook=_unique_object,
                        parse_float=_finite_float,
                        parse_constant=_reject_constant,
                    )
                else:
                    try:
                        import yaml
                    except ImportError as exc:
                        raise ConfigurationError(
                            "PyYAML is required to parse YAML specifications"
                        ) from exc
                    try:

                        class UniqueSafeLoader(yaml.SafeLoader):
                            pass

                        def construct_mapping(loader, node, deep=False):
                            loader.flatten_mapping(node)
                            return _unique_object(
                                (
                                    loader.construct_object(key, deep=deep),
                                    loader.construct_object(value, deep=deep),
                                )
                                for key, value in node.value
                            )

                        UniqueSafeLoader.add_constructor(
                            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
                        )
                        spec = yaml.load(source, Loader=UniqueSafeLoader)
                    except yaml.YAMLError as exc:
                        raise ConfigurationError(f"Invalid YAML specification: {exc}") from exc
        except (OSError, ValueError) as exc:
            raise ConfigurationError(f"Unable to read specification {filepath}: {exc}") from exc
        if not isinstance(spec, dict):
            raise ConfigurationError("Pipeline specification must be a mapping")
        return spec
