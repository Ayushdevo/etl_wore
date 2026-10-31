import pytest
from etl_wore.loaders.csv_loader import CsvLoader
from etl_wore.exceptions import LoadingError

class BrokenCell:
    def __str__(self): raise ValueError('cannot format cell')

@pytest.mark.parametrize('value', ['\ud800', BrokenCell()])
def test_later_cell_serialization_failure_leaves_csv_unchanged(tmp_path, value):
    path = tmp_path / 'data.csv'
    path.write_text('name\noriginal\n')
    before = path.read_bytes()
    with pytest.raises(LoadingError):
        CsvLoader(str(path)).load([{'name':'valid'}, {'name':value}])
    assert path.read_bytes() == before
