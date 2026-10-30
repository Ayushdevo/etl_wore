from unittest.mock import patch
import pytest
from etl_wore.builder import _component, _EXTRACTORS
from etl_wore.exceptions import ConfigurationError


def test_rest_source_forwards_pagination_and_headers():
    source = _component({"type": "rest", "endpoint": "https://example.test/items", "headers": {"X-Test": "ok"}, "page_param": "p"}, _EXTRACTORS, "source")
    with patch("etl_wore.extractors.api_extractor.requests.get") as get:
        get.return_value.json.side_effect = [[{"id": 1}], []]
        assert list(source.extract()) == [{"id": 1}]
        assert get.call_args.kwargs == {"headers": {"X-Test": "ok"}, "params": {"p": 2}, "timeout": 10}


@pytest.mark.parametrize("endpoint", ["file:///etc/passwd", "ftp://example.test/a", "https://", 42])
def test_rest_only_accepts_http_endpoints(endpoint):
    with pytest.raises(ConfigurationError, match="endpoint"):
        _component({"type": "rest", "endpoint": endpoint}, _EXTRACTORS, "source")
