import pytest
from etl_wore.transformers.schema_validator import SchemaValidator
from etl_wore.exceptions import TransformationError

@pytest.mark.parametrize('value', [float('nan'), float('inf'), 'NaN', '1e9999'])
@pytest.mark.parametrize('drop', [False, True])
def test_float_schema_rejects_nonfinite_values(value, drop):
    validator = SchemaValidator({'value':float}, drop_invalid=drop)
    if drop:
        assert validator.transform({'value':value}) is None
    else:
        with pytest.raises(TransformationError, match='finite'):
            validator.transform({'value':value})
