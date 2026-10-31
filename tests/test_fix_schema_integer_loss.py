import pytest
from etl_wore.transformers.schema_validator import SchemaValidator
from etl_wore.exceptions import TransformationError

@pytest.mark.parametrize('value', [1.5, -2.7])
@pytest.mark.parametrize('drop', [False, True])
def test_fractional_numbers_cannot_be_silently_truncated(value, drop):
    validator = SchemaValidator({'count':int}, drop_invalid=drop)
    if drop:
        assert validator.transform({'count':value}) is None
    else:
        with pytest.raises(TransformationError, match='fractional'):
            validator.transform({'count':value})

def test_integral_float_and_integer_string_remain_supported():
    validator = SchemaValidator({'count':int})
    assert validator.transform({'count':2.0}) == {'count':2}
    assert validator.transform({'count':'2'}) == {'count':2}
