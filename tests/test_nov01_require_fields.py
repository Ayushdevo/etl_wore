import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError, TransformationError


def build(**options):
    return _component(
        dict(type="require_fields", **options), _TRANSFORMERS, "transformer"
    )


def test_required_fields_have_explicit_error_or_drop_behavior():
    transform = build(fields=["id"])
    assert transform.transform({"id": 0}) == {"id": 0}
    with pytest.raises(TransformationError):
        transform.transform({"id": None})
    assert build(fields=["id"], drop_invalid=True).transform({}) is None
    assert build(fields=["id"], allow_null=True).transform({"id": None}) == {"id": None}


def test_invalid_drop_flag():
    with pytest.raises(ConfigurationError):
        build(fields=["id"], drop_invalid="true")
