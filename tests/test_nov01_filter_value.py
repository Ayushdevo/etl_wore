import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError


def build(**options):
    return _component(
        dict(type="filter_value", **options), _TRANSFORMERS, "transformer"
    )


def test_filter_distinguishes_null_missing_boolean_and_zero():
    transform = build(field="active", value=True)
    assert transform.transform({"active": True}) == {"active": True}
    assert transform.transform({"active": 1}) is None
    assert build(field="a", value=None).transform({}) is None
    assert build(field="a", value=None).transform({"a": None}) == {"a": None}
    assert build(field="a", value=1, exclude=True).transform({"a": 2}) == {"a": 2}


def test_invalid_exclude_flag():
    with pytest.raises(ConfigurationError):
        build(field="a", value=1, exclude=1)
