from unittest.mock import patch
from urllib.parse import urlsplit, parse_qsl
from etl_wore.extractors.api_extractor import RestApiExtractor
def test_existing_page_is_replaced_without_losing_repeated_filters():
    source = RestApiExtractor('https://example.test/jobs?page=9&tag=a&tag=b')
    with patch('etl_wore.extractors.api_extractor.requests.get') as get:
        source._fetch_page(2)
    args, kwargs = get.call_args
    pairs = parse_qsl(urlsplit(args[0]).query) + list(kwargs['params'])
    assert pairs == [('tag', 'a'), ('tag', 'b'), ('page', 2)]
