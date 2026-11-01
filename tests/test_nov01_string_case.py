import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="string_case", **options), _TRANSFORMERS, "transformer")


def test_unicode_case_and_nullable_fields():
    assert build(fields=["name"]).transform({"name": "Straße"}) == {"name": "strasse"}
    assert build(fields=["name"], mode="upper").transform({"name": "hello"}) == {
        "name": "HELLO"
    }
    assert build(fields=["name"]).transform({"name": None}) == {"name": None}
    with pytest.raises(TransformationError):
        build(fields=["name"]).transform({"name": 42})


def test_invalid_mode():
    with pytest.raises(ConfigurationError):
        build(fields=["a"], mode="capitalize")
