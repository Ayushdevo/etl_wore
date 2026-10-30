import pytest
from etl_wore.extractors.json_extractor import JsonExtractor


@pytest.mark.parametrize("text,is_lines", [('[{"name":"café"}]', False), ('{"name":"café"}\n', True)])
def test_default_json_encoding_accepts_a_utf8_bom(tmp_path, text, is_lines):
    path = tmp_path / "records.json"
    path.write_text(text, encoding="utf-8-sig")
    assert list(JsonExtractor(str(path), is_lines=is_lines).extract()) == [{"name": "café"}]
