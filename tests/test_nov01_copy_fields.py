import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="copy_fields", **options), _TRANSFORMERS, "transformer")


def test_copy_uses_original_values_and_independent_containers():
    source = {"a": [1], "b": [2]}
    result = build(mapping={"a": "b", "b": "c"}, overwrite=True).transform(source)
    assert result == {"a": [1], "b": [1], "c": [2]}
    result["b"].append(3)
    assert result["a"] == [1] and source["a"] == [1]
    with pytest.raises(TransformationError):
        build(mapping={"a": "b"}).transform(source)


def test_bad_mapping():
    with pytest.raises(ConfigurationError):
        build(mapping={"a": "c", "b": "c"})
