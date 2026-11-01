import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="flatten", **options), _TRANSFORMERS, "transformer")


def test_flatten_preserves_lists_empty_objects_and_input_ownership():
    source = {"person": {"name": "Ada", "meta": {}}, "tags": ["a"]}
    result = build().transform(source)
    assert result == {"person.name": "Ada", "person.meta": {}, "tags": ["a"]}
    result["tags"].append("b")
    assert source["tags"] == ["a"]


def test_ambiguous_and_recursive_objects_are_rejected():
    with pytest.raises(TransformationError):
        build().transform({"a.b": 1})
    cycle = {}
    cycle["self"] = cycle
    with pytest.raises(TransformationError):
        build().transform(cycle)


def test_bad_separator():
    with pytest.raises(ConfigurationError):
        build(separator="")


def test_overlapping_multichar_separator_cannot_produce_ambiguous_paths():
    with pytest.raises(TransformationError, match="ambiguous"):
        build(separator="aa").transform({"a": {"a": 1}})
    assert build(separator="::").transform({"person": {"name": "Ada"}}) == {
        "person::name": "Ada"
    }
