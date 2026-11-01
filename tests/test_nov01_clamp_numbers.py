import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="clamp_numbers", **options), _TRANSFORMERS, "transformer"
    )


def test_one_and_two_sided_clamping():
    assert build(fields=["value"], minimum=0, maximum=10).transform({"value": 12}) == {
        "value": 10
    }
    assert build(fields=["value"], minimum=0).transform({"value": -2}) == {"value": 0}
    with pytest.raises(TransformationError):
        build(fields=["value"], maximum=1).transform({"value": float("nan")})


def test_invalid_bounds():
    for options in ({}, {"minimum": 2, "maximum": 1}, {"minimum": True}):
        with pytest.raises(ConfigurationError):
            build(fields=["a"], **options)
