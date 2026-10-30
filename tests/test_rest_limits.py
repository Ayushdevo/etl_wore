from unittest.mock import Mock, patch

import pytest

from etl_wore.builder import _EXTRACTORS, _component
from etl_wore.exceptions import ExtractionError
from etl_wore.extractors.api_extractor import RestApiExtractor


def test_nonterminating_endpoint_stops_at_request_limit():
    source = _component(
        {"type": "rest", "endpoint": "https://example.test/items", "max_pages": 2},
        _EXTRACTORS,
        "source",
    )
    source._fetch_page = Mock(return_value=[{"id": 1}])
    with pytest.raises(ExtractionError, match="max_pages=2"):
        list(source.extract())
    assert source._fetch_page.call_count == 2


def test_empty_terminal_page_within_limit_succeeds():
    source = RestApiExtractor("https://example.test/items", max_pages=2)
    source._fetch_page = Mock(side_effect=[[{"id": 1}], []])
    assert list(source.extract()) == [{"id": 1}]


@pytest.mark.parametrize("limit", [0, -1, True, 1.5, "2"])
def test_request_limit_is_a_positive_integer(limit):
    with pytest.raises(ValueError):
        RestApiExtractor("https://example.test/items", max_pages=limit)


def test_timeout_is_forwarded_to_each_request():
    source = _component(
        {"type": "rest", "endpoint": "https://example.test/items", "timeout": 0.25},
        _EXTRACTORS,
        "source",
    )
    with patch("etl_wore.extractors.api_extractor.requests.get") as get:
        get.return_value.json.return_value = []
        assert list(source.extract()) == []
        assert get.call_args.kwargs["timeout"] == 0.25


@pytest.mark.parametrize("timeout", [0, -1, True, float("nan"), float("inf"), "10"])
def test_invalid_timeout_is_rejected_before_network(timeout):
    with pytest.raises(ValueError):
        RestApiExtractor("https://example.test/items", timeout=timeout)


def test_timeout_too_large_for_float_is_a_value_error():
    with pytest.raises(ValueError, match="timeout"):
        RestApiExtractor("https://example.test/items", timeout=10**1000)
