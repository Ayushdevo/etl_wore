import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(dict(type="unflatten", **options), _TRANSFORMERS, "transformer")


def test_flatten_roundtrip_and_empty_objects():
    from etl_wore.transformers.flatten import FlattenRecord

    source = {"a": {"b": 1, "empty": {}}, "list": [1, 2]}
    assert build().transform(FlattenRecord().transform(source)) == source


@pytest.mark.parametrize(
    "source", [{"a": 1, "a.b": 2}, {"a.b": 2, "a": 1}, {"a": {}, "a.b": 2}, {"a..b": 1}]
)
def test_conflicts_are_rejected_independently_of_input_order(source):
    with pytest.raises(TransformationError):
        build().transform(source)


def test_bad_separator():
    with pytest.raises(ConfigurationError):
        build(separator=None)
