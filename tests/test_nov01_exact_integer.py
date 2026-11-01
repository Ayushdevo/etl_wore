from decimal import Decimal
from fractions import Fraction

import pytest

from etl_wore.exceptions import TransformationError
from etl_wore.transformers.schema_validator import SchemaValidator


@pytest.mark.parametrize("value", [Decimal("1.5"), Fraction(3, 2)])
def test_non_float_fractional_values_are_not_truncated(value):
    with pytest.raises(TransformationError):
        SchemaValidator({"n": int}).transform({"n": value})
    assert (
        SchemaValidator({"n": int}, drop_invalid=True).transform({"n": value}) is None
    )


@pytest.mark.parametrize("value", [Decimal("2"), Fraction(4, 2), "2", 2.0])
def test_lossless_integers_remain_supported(value):
    assert SchemaValidator({"n": int}).transform({"n": value}) == {"n": 2}
