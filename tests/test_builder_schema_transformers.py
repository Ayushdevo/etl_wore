import pytest

from etl_wore.builder import _TRANSFORMERS, _component
from etl_wore.exceptions import ConfigurationError


def test_schema_casts_serializable_types_and_drops_invalid_rows():
    stage = _component(
        {"type": "schema", "schema": {"age": "int", "active": "bool"}, "drop_invalid": True},
        _TRANSFORMERS,
        "stage",
    )
    assert stage.transform({"age": "21", "active": "false"}) == {"age": 21, "active": False}
    assert stage.transform({"age": "bad", "active": "true"}) is None


@pytest.mark.parametrize("schema", [{}, {"age": "eval"}, {"age": None}, {"": "int"}])
def test_schema_uses_a_closed_type_vocabulary(schema):
    with pytest.raises(ConfigurationError, match="schema"):
        _component({"type": "schema", "schema": schema}, _TRANSFORMERS, "stage")
