import pytest
from etl_wore.loaders.json_loader import JsonLinesLoader
from etl_wore.exceptions import LoadingError

@pytest.mark.parametrize('record', [{1:'number', '1':'string'}, {'nested':[{False:'bad'}]}])
def test_nonstring_json_keys_cannot_silently_change_identity(tmp_path, record):
    path = tmp_path / 'output.jsonl'
    path.write_text('{"original":true}\n')
    before = path.read_bytes()
    with pytest.raises(LoadingError, match='keys'):
        JsonLinesLoader(str(path)).load([{'ok':True}, record])
    assert path.read_bytes() == before
