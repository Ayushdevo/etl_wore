import pytest
from etl_wore.extractors.json_extractor import JsonExtractor
from etl_wore.exceptions import ExtractionError

@pytest.mark.parametrize('lines', [False, True])
@pytest.mark.parametrize('content', ['{"id":1,"id":2}', '{"nested":{"id":1,"id":2}}'])
def test_duplicate_json_keys_are_rejected(tmp_path, lines, content):
    path = tmp_path / 'input.json'
    path.write_text(content)
    with pytest.raises(ExtractionError, match='Duplicate'):
        list(JsonExtractor(str(path), is_lines=lines).extract())

def test_repeated_keys_in_distinct_records_are_valid(tmp_path):
    path = tmp_path / 'input.json'
    path.write_text('[{"id":1},{"id":2}]')
    assert list(JsonExtractor(str(path)).extract()) == [{'id':1}, {'id':2}]
