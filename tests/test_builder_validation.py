from copy import deepcopy

import pytest

from etl_wore.builder import build_pipeline, validate_spec
from etl_wore.exceptions import ConfigurationError


def envelope():
    return {"name": "demo", "extractors": [{"type": "csv"}], "loaders": [{"type": "jsonl"}]}


@pytest.mark.parametrize(
    "change",
    [
        {"name": " "},
        {"batch_size": True},
        {"batch_size": 0},
        {"batch_size": "2"},
        {"extractors": []},
        {"loaders": []},
        {"transformers": {}},
        {"extractors": [None]},
        {"loaders": [{"type": 2}]},
        {"typo": True},
    ],
)
def test_invalid_envelope_is_rejected(change):
    spec = envelope()
    spec.update(change)
    with pytest.raises(ConfigurationError):
        validate_spec(spec)


def test_envelope_is_not_mutated():
    spec = envelope()
    before = deepcopy(spec)
    validate_spec(spec)
    assert spec == before


def test_arbitrary_imports_are_not_a_component_type():
    spec = envelope()
    spec["extractors"] = [{"type": "os.system", "command": "echo unsafe"}]
    with pytest.raises(ConfigurationError, match="unsupported component type"):
        build_pipeline(spec)
