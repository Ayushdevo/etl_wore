import pytest

from etl_wore.transformers.schema_validator import SchemaValidator


def test_schema_is_snapshotted():
    schema = {"id": int}
    validator = SchemaValidator(schema)
    schema["id"] = str
    assert validator.transform({"id": "2"}) == {"id": 2}


@pytest.mark.parametrize("schema", [None, [], {"id": "int"}, {"": int}, {"id": object}])
def test_invalid_schema_fails_at_construction(schema):
    with pytest.raises(ValueError):
        SchemaValidator(schema)


def test_invalid_drop_flag():
    with pytest.raises(ValueError):
        SchemaValidator({"id": int}, drop_invalid="false")
