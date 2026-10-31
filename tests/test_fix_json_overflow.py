import pytest
from etl_wore.extractors.json_extractor import JsonExtractor
from etl_wore.exceptions import ExtractionError

@pytest.mark.parametrize('lines', [False, True])
def test_exponent_overflow_is_not_accepted_as_infinity(tmp_path, lines):
    path = tmp_path / 'input.json'
    path.write_text('{"value":1e9999}')
    with pytest.raises(ExtractionError, match='finite'):
        list(JsonExtractor(str(path), is_lines=lines).extract())
