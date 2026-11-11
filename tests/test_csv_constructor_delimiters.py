import pytest
from etl_wore.extractors.csv_extractor import CsvExtractor
from etl_wore.loaders.csv_loader import CsvLoader
@pytest.mark.parametrize('delimiter', ['', 'ab', 1, '\n', '\r', '\x00'])
@pytest.mark.parametrize('factory', [CsvExtractor, CsvLoader])
def test_invalid_delimiters_fail_before_io(factory, delimiter):
    with pytest.raises(ValueError):
        factory('unused.csv', delimiter=delimiter)
