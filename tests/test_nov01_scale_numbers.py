import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="scale_numbers", **options), _TRANSFORMERS, "transformer"
    )


def test_affine_scaling_and_overflow_detection():
    assert build(fields=["temp"], factor=1.8, offset=32).transform({"temp": 0}) == {
        "temp": 32.0
    }
    for bad in (True, float("nan"), "2"):
        with pytest.raises(TransformationError):
            build(fields=["temp"]).transform({"temp": bad})
    with pytest.raises(TransformationError):
        build(fields=["temp"], factor=1e308).transform({"temp": 1e308})


def test_nonfinite_factor():
    with pytest.raises(ConfigurationError):
        build(fields=["a"], factor=float("inf"))
