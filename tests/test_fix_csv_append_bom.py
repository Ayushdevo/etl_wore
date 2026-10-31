from etl_wore.loaders.csv_loader import CsvLoader
from etl_wore.extractors.csv_extractor import CsvExtractor

def test_append_recognizes_bom_prefixed_header(tmp_path):
    path = tmp_path / 'data.csv'
    path.write_text('name,age\nAlice,20\n', encoding='utf-8-sig')
    CsvLoader(str(path)).load([{'name':'Bob','age':21}])
    assert list(CsvExtractor(str(path)).extract()) == [
        {'name':'Alice','age':'20'}, {'name':'Bob','age':'21'}]
    assert path.read_bytes().count(b'\xef\xbb\xbf') == 1
