import pytest
from etl_wore.loaders.json_loader import JsonLinesLoader
from etl_wore.exceptions import LoadingError

def test_unencodable_later_record_cannot_append_earlier_records(tmp_path):
    path = tmp_path / 'data.jsonl'
    path.write_text('{"old":true}\n')
    before = path.read_bytes()
    with pytest.raises(LoadingError):
        JsonLinesLoader(str(path)).load([{'ok':True}, {'bad':'\ud800'}])
    assert path.read_bytes() == before
