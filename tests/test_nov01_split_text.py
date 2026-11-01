import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="split_text", **options), _TRANSFORMERS, "transformer")


def test_literal_split_keeps_empty_components():
    assert build(fields=["tags"], separator=",").transform({"tags": "a,,b"}) == {
        "tags": ["a", "", "b"]
    }
    assert build(fields=["tags"], separator=",", maxsplit=1).transform(
        {"tags": "a,b,c"}
    ) == {"tags": ["a", "b,c"]}
    with pytest.raises(TransformationError):
        build(fields=["tags"], separator=",").transform({"tags": 1})


def test_empty_separator_is_rejected():
    with pytest.raises(ConfigurationError):
        build(fields=["a"], separator="")
