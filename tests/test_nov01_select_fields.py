import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="select_fields", **options), _TRANSFORMERS, "transformer"
    )


def test_projection_order_missing_and_input_ownership():
    source = {"a": [1], "b": 2}
    result = build(fields=["b", "a", "absent"]).transform(source)
    assert list(result) == ["b", "a"]
    result["a"].append(3)
    assert source["a"] == [1]
    with pytest.raises(TransformationError):
        build(fields=["absent"], require_all=True).transform(source)


@pytest.mark.parametrize("fields", ["abc", [], ["a", "a"], [1]])
def test_invalid_projection(fields):
    with pytest.raises(ConfigurationError):
        build(fields=fields)
