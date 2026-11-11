import pytest
from etl_wore.transformers.sanitizer import DataSanitizer
from etl_wore.exceptions import TransformationError
def test_output_does_not_alias_nested_input():
    original = {'id': 1, 'date': '2026-01-01', 'nested': {'items': [1]}}
    output = DataSanitizer().transform(original)
    output['nested']['items'].append(2)
    assert original['nested']['items'] == [1]
@pytest.mark.parametrize('record', [None, [], 'text'])
def test_non_object_records_raise_transformation_error(record):
    with pytest.raises(TransformationError):
        DataSanitizer().transform(record)
