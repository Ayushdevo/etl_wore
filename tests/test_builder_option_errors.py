import pytest

from etl_wore.builder import _EXTRACTORS, _component, build_pipeline
from etl_wore.exceptions import ConfigurationError


def test_oversized_timeout_is_a_configuration_error():
    with pytest.raises(ConfigurationError, match="timeout"):
        _component(
            {"type": "rest", "endpoint": "https://example.test", "timeout": 10**1000},
            _EXTRACTORS,
            "source",
        )


@pytest.mark.parametrize("path", ["bad\0name", "bad\0name/child"])
def test_invalid_paths_are_configuration_errors(tmp_path, path):
    spec = {
        "name": "bad",
        "extractors": [{"type": "json", "filepath": path}],
        "loaders": [{"type": "jsonl", "output_path": "out.jsonl"}],
    }
    with pytest.raises(ConfigurationError, match="filepath"):
        build_pipeline(spec, base_dir=tmp_path)
    assert not (tmp_path / "out.jsonl").exists()
