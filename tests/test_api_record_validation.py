from unittest.mock import Mock

import pytest

from etl_wore.exceptions import ExtractionError
from etl_wore.extractors.api_extractor import RestApiExtractor


@pytest.mark.parametrize("payload", [None, 42, "error", {"items": None}, {"data": {"id": 1}}, [42], [{"id": 1}, None]])
def test_invalid_page_is_rejected_before_yielding(payload):
    extractor = RestApiExtractor("https://example.invalid/records")
    extractor._fetch_page = Mock(return_value=payload)
    with pytest.raises(ExtractionError, match="page 1"):
        next(extractor.extract())
    extractor._fetch_page.assert_called_once_with(1)


@pytest.mark.parametrize("envelope", [lambda items: items, lambda items: {"items": items}, lambda items: {"data": items}])
def test_supported_pages_and_empty_termination(envelope):
    extractor = RestApiExtractor("https://example.invalid/records")
    extractor._fetch_page = Mock(side_effect=[envelope([{"id": 1}]), envelope([])])
    assert list(extractor.extract()) == [{"id": 1}]
    assert [call.args for call in extractor._fetch_page.call_args_list] == [(1,), (2,)]


def test_malformed_later_page_reports_its_number():
    extractor = RestApiExtractor("https://example.invalid/records")
    extractor._fetch_page = Mock(side_effect=[[{"id": 1}], {"items": "bad"}])
    records = extractor.extract()
    assert next(records) == {"id": 1}
    with pytest.raises(ExtractionError, match="page 2"):
        next(records)
