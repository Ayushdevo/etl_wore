import pytest
from unittest.mock import Mock
from etl_wore.extractors.api_extractor import RestApiExtractor
from etl_wore.exceptions import ExtractionError
@pytest.mark.parametrize('payload', [None, 1, 'text', {}, {'items': None}, {'items': {}}, {'data': 'abc'}, [{'id': 1}, 2]])
def test_malformed_pages_fail_before_any_record_is_yielded(payload):
    source = RestApiExtractor('https://example.test', max_pages=1)
    source._fetch_page = Mock(return_value=payload)
    with pytest.raises(ExtractionError):
        next(source.extract())
@pytest.mark.parametrize('payload', [[], {'items': []}, {'data': []}])
def test_empty_collections_end_pagination(payload):
    source = RestApiExtractor('https://example.test')
    source._fetch_page = Mock(return_value=payload)
    assert list(source.extract()) == []
