import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError


def build(**options):
    return _component(dict(type="defaults", **options), _TRANSFORMERS, "transformer")


def test_defaults_preserve_falsey_values_and_own_nested_values():
    values = {"a": [1], "b": 2, "c": 3}
    transform = build(values=values)
    values["a"].append(9)
    result = transform.transform({"b": 0, "c": None})
    assert result == {"a": [1], "b": 0, "c": None}
    result["a"].append(2)
    assert transform.transform({})["a"] == [1]
    assert build(values={"c": 3}, replace_null=True).transform({"c": None}) == {"c": 3}


def test_bad_defaults():
    with pytest.raises(ConfigurationError):
        build(values=[])
