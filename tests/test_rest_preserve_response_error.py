import pytest
from unittest.mock import Mock, patch
from etl_wore.extractors.api_extractor import RestApiExtractor
def test_close_failure_does_not_hide_json_failure():
    response = Mock()
    response.json.side_effect = ValueError('bad JSON')
    response.close.side_effect = RuntimeError('close failed')
    with patch('etl_wore.extractors.api_extractor.requests.get', return_value=response):
        with pytest.raises(ValueError, match='bad JSON'):
            RestApiExtractor('https://example.test')._fetch_page(1)
    response.close.assert_called_once()
def test_close_failure_is_reported_after_success():
    response = Mock()
    response.close.side_effect = RuntimeError('close failed')
    with patch('etl_wore.extractors.api_extractor.requests.get', return_value=response):
        with pytest.raises(RuntimeError, match='close failed'):
            RestApiExtractor('https://example.test')._fetch_page(1)
