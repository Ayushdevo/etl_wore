import pytest
from etl_wore.extractors.json_extractor import JsonExtractor
@pytest.mark.parametrize('mode', ['false', 1, [], None])
def test_lines_mode_requires_explicit_boolean(mode):
    with pytest.raises(ValueError):
        JsonExtractor('unused.json', is_lines=mode)
