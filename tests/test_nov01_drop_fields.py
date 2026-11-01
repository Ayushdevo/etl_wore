import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError


def build(**options):
    return _component(dict(type="drop_fields", **options), _TRANSFORMERS, "transformer")


def test_drop_is_idempotent_and_does_not_modify_input():
    source = {"private": "secret", "keep": [1]}
    transform = build(fields=["private", "absent"])
    result = transform.transform(source)
    assert result == {"keep": [1]}
    assert transform.transform(result) == result
    result["keep"].append(2)
    assert source["keep"] == [1] and "private" in source


def test_bad_fields():
    with pytest.raises(ConfigurationError):
        build(fields="private")
