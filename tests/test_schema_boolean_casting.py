import pytest
from etl_wore.transformers.schema_validator import SchemaValidator
from etl_wore.exceptions import TransformationError

@pytest.mark.parametrize("raw, expected", [("false", False), ("TRUE", True), (" 0 ", False), ("1", True), (0, False), (1, True)])
def test_boolean_cast(raw, expected):
    assert SchemaValidator({"enabled": bool}).transform({"enabled":raw})["enabled"] is expected

def test_unknown_boolean_is_invalid():
    with pytest.raises(TransformationError):
        SchemaValidator({"enabled":bool}).transform({"enabled":"maybe"})
    assert SchemaValidator({"enabled":bool}, drop_invalid=True).transform({"enabled":"maybe"}) is None
