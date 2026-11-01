from unittest.mock import Mock, patch

import pytest

from etl_wore.extractors.api_extractor import RestApiExtractor


@pytest.mark.parametrize("failure", [False, True])
def test_response_is_always_closed(failure):
    response = Mock()
    response.json.return_value = []
    if failure:
        response.json.side_effect = ValueError("invalid JSON")
    with patch(
        "etl_wore.extractors.api_extractor.requests.get", return_value=response
    ), patch("etl_wore.utils.retry.time.sleep"):
        if failure:
            with pytest.raises(ValueError):
                RestApiExtractor("https://example.test")._fetch_page(1)
        else:
            assert RestApiExtractor("https://example.test")._fetch_page(1) == []
    assert response.close.call_count == response.json.call_count
