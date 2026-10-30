import pytest
from etl_wore.builder import _component, _EXTRACTORS
from etl_wore.exceptions import ConfigurationError


def test_csv_source_preserves_quoted_delimiters(tmp_path):
    source = tmp_path / "source.csv"
    source.write_text('id;name\n1;"Doe; Jane"\n')
    extractor = _component({"type": "csv", "filepath": str(source), "delimiter": ";"}, _EXTRACTORS, "extractors[0]")
    assert list(extractor.extract()) == [{"id": "1", "name": "Doe; Jane"}]


@pytest.mark.parametrize("options", [{}, {"filepath": "x", "delimiter": "||"}, {"filepath": "x", "encoding": "not-an-encoding"}, {"filepath": "x", "delimter": ","}])
def test_csv_source_bad_options(options):
    with pytest.raises(ConfigurationError, match="extractors\[0\]"):
        _component(dict(type="csv", **options), _EXTRACTORS, "extractors[0]")
