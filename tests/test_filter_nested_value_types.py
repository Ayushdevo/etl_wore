import pytest
from etl_wore.transformers.filter_value import FilterValue
@pytest.mark.parametrize('expected,actual', [([True], [1]), ({'x': False}, {'x': 0}), ([{'x': [True]}], [{'x': [1]}])])
def test_nested_booleans_do_not_match_numbers(expected, actual):
    assert FilterValue('x', expected).transform({'x': actual}) is None
    assert FilterValue('x', expected).transform({'x': expected}) == {'x': expected}
