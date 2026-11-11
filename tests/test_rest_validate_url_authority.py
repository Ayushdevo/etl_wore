import pytest
from etl_wore.extractors.api_extractor import RestApiExtractor
@pytest.mark.parametrize('url', ['https://example.test:bad', 'https://example.test:65536', 'https://exa mple.test', 'https://example.test/	jobs', 'https://example.test\\evil'])
def test_bad_url_fails_before_network(url):
    with pytest.raises(ValueError):
        RestApiExtractor(url)
