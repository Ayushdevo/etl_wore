import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="rename_fields", **options), _TRANSFORMERS, "transformer"
    )


def test_simultaneous_rename_supports_swaps():
    source = {"a": 1, "b": 2}
    assert build(mapping={"a": "b", "b": "a"}).transform(source) == {"b": 1, "a": 2}
    assert source == {"a": 1, "b": 2}
    with pytest.raises(TransformationError):
        build(mapping={"a": "b"}).transform(source)


def test_duplicate_destinations_and_bad_mapping_fail():
    for mapping in ({"a": "c", "b": "c"}, {"a": 1}, {}):
        with pytest.raises(ConfigurationError):
            build(mapping=mapping)
