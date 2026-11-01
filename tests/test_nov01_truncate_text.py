import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="truncate_text", **options), _TRANSFORMERS, "transformer"
    )


def test_unicode_codepoint_truncation_and_zero_length():
    assert build(fields=["name"], max_length=2).transform({"name": "é你好"}) == {
        "name": "é你"
    }
    assert build(fields=["name"], max_length=0).transform({"name": "abc"}) == {
        "name": ""
    }
    with pytest.raises(TransformationError):
        build(fields=["name"], max_length=2).transform({"name": 12})


@pytest.mark.parametrize("length", [-1, True, 1.5])
def test_bad_length(length):
    with pytest.raises(ConfigurationError):
        build(fields=["a"], max_length=length)
