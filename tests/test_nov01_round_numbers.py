import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="round_numbers", **options), _TRANSFORMERS, "transformer"
    )


def test_rounding_uses_python_ties_to_even():
    assert build(fields=["value"], digits=1).transform({"value": 1.25}) == {
        "value": 1.2
    }
    assert build(fields=["value"], digits=-1).transform({"value": 125}) == {
        "value": 120
    }
    with pytest.raises(TransformationError):
        build(fields=["value"]).transform({"value": True})


def test_bad_digits():
    with pytest.raises(ConfigurationError):
        build(fields=["a"], digits=True)
