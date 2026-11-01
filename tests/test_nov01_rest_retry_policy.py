from unittest.mock import Mock, patch

import pytest
import requests

from etl_wore.extractors.api_extractor import RestApiExtractor


@pytest.mark.parametrize(
    "status,retryable", [(400, False), (401, False), (429, True), (503, True)]
)
def test_http_retry_policy(status, retryable):
    bad = Mock(status_code=status)
    bad.raise_for_status.side_effect = requests.HTTPError("HTTP error")
    good = Mock(status_code=200)
    good.json.return_value = []
    with patch(
        "etl_wore.extractors.api_extractor.requests.get", side_effect=[bad, good]
    ) as get, patch("etl_wore.utils.retry.time.sleep"):
        source = RestApiExtractor("https://example.test")
        if retryable:
            assert source._fetch_page(1) == []
        else:
            with pytest.raises(requests.HTTPError):
                source._fetch_page(1)
        assert get.call_count == (2 if retryable else 1)


def test_bad_json_is_not_retried():
    response = Mock()
    response.json.side_effect = ValueError("bad json")
    with patch(
        "etl_wore.extractors.api_extractor.requests.get", return_value=response
    ) as get, patch("etl_wore.utils.retry.time.sleep"):
        with pytest.raises(ValueError):
            RestApiExtractor("https://example.test")._fetch_page(1)
        assert get.call_count == 1
