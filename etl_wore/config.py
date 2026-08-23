"""
Configuration management and environment variable parsing.
"""
import os
from typing import Any, Dict

class Config:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._settings = defaults or {}

    def get(self, key: str, default: Any = None) -> Any:
        # Check environment variable first, capitalized with ETL_ prefix
        env_key = f"ETL_{key.upper()}"
        if env_key in os.environ:
            return os.environ[env_key]
        return self._settings.get(key, default)

    def set(self, key: str, value: Any):
        self._settings[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._settings)
