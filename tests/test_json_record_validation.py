import pytest
from etl_wore.extractors.json_extractor import JsonExtractor
from etl_wore.exceptions import ExtractionError

@pytest.mark.parametrize("lines,text", [(False, '[{"id":1},42]'), (True, '{"id":1}\nnull\n'), (True, '[1,2]\n')])
def test_json_records_must_be_objects(tmp_path, lines, text):
    path = tmp_path / "data.json"
    path.write_text(text)
    with pytest.raises(ExtractionError):
        list(JsonExtractor(str(path), is_lines=lines).extract())
