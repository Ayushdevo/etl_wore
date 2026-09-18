"""
Declarative JSON/YAML pipeline specification parser.
"""
import json
import os
from typing import Dict, Any
from .exceptions import ConfigurationError

class SpecParser:
    @staticmethod
    def parse_file(filepath: str) -> Dict[str, Any]:
        if not os.path.exists(filepath):
            raise ConfigurationError(f"Spec file not found: {filepath}")

        ext = os.path.splitext(filepath)[1].lower()
        with open(filepath, "r", encoding="utf-8") as f:
            if ext in [".yaml", ".yml"]:
                try:
                    import yaml
                    return yaml.safe_load(f)
                except ImportError:
                    raise ConfigurationError("PyYAML is required to parse YAML specifications")
            elif ext == ".json":
                return json.load(f)
            else:
                raise ConfigurationError(f"Unsupported spec format: {ext}")
