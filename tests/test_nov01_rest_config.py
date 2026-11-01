from unittest.mock import patch

import pytest

from etl_wore.extractors.api_extractor import RestApiExtractor


@pytest.mark.parametrize(
    "options",
    [
        {"endpoint": "file:///tmp/x"},
        {"endpoint": "http://"},
        {"endpoint": "https://example.test", "page_param": ""},
        {"endpoint": "https://example.test", "headers": {"A": 1}},
    ],
)
def test_invalid_request_settings_fail_at_construction(options):
    with pytest.raises(ValueError):
        RestApiExtractor(**options)


def test_headers_are_snapshotted():
    headers = {"Authorization": "token"}
    source = RestApiExtractor("https://example.test", headers=headers)
    headers.clear()
    with patch("etl_wore.extractors.api_extractor.requests.get") as get:
        source._fetch_page(1)
        assert get.call_args.kwargs["headers"] == {"Authorization": "token"}
