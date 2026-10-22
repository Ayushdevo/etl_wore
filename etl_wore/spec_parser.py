"""Declarative JSON/YAML pipeline specification parser."""
import json
import os
from typing import Dict, Any
from .exceptions import ConfigurationError

class SpecParser:
    @staticmethod
    def parse_file(filepath: str) -> Dict[str, Any]:
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in {".json", ".yaml", ".yml"}:
            raise ConfigurationError(f"Unsupported spec format: {ext}")
        try:
            with open(filepath, "r", encoding="utf-8") as source:
                if ext == ".json":
                    spec = json.load(source)
                else:
                    try:
                        import yaml
                    except ImportError as exc:
                        raise ConfigurationError("PyYAML is required to parse YAML specifications") from exc
                    try:
                        spec = yaml.safe_load(source)
                    except yaml.YAMLError as exc:
                        raise ConfigurationError(f"Invalid YAML specification: {exc}") from exc
        except (OSError, ValueError) as exc:
            raise ConfigurationError(f"Unable to read specification {filepath}: {exc}") from exc
        if not isinstance(spec, dict):
            raise ConfigurationError("Pipeline specification must be a mapping")
        return spec
