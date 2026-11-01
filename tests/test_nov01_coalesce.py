import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError


def build(**options):
    return _component(dict(type="coalesce", **options), _TRANSFORMERS, "transformer")


def test_coalescing_preserves_zero_and_respects_order():
    assert (
        build(fields=["a", "b"], target="value").transform({"a": 0, "b": 2})["value"]
        == 0
    )
    assert (
        build(fields=["a", "b"], target="value", skip_empty=True).transform(
            {"a": "", "b": "ok"}
        )["value"]
        == "ok"
    )
    assert build(fields=["missing"], target="value").transform({}) == {}


def test_bad_target():
    with pytest.raises(ConfigurationError):
        build(fields=["a"], target="")
