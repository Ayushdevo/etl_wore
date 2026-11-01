import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="join_text", **options), _TRANSFORMERS, "transformer")


def test_join_does_not_coerce_or_iterate_a_scalar_string():
    assert build(fields=["tags"], separator=" / ").transform({"tags": ["a", "b"]}) == {
        "tags": "a / b"
    }
    assert build(fields=["tags"]).transform({"tags": []}) == {"tags": ""}
    for bad in ("abc", [1], {"a": "b"}):
        with pytest.raises(TransformationError):
            build(fields=["tags"]).transform({"tags": bad})


def test_bad_separator():
    with pytest.raises(ConfigurationError):
        build(fields=["a"], separator=None)
