from etl_wore.builder import build_pipeline


def test_sqlite_distinct_unicode_tables_are_allowed(tmp_path):
    spec = {
        "name": "unicode",
        "extractors": [{"type": "json", "filepath": "source.json"}],
        "loaders": [
            {"type": "sqlite", "db_path": "data.db", "table_name": "Ä"},
            {"type": "sqlite", "db_path": "data.db", "table_name": "ä"},
        ],
    }
    pipeline = build_pipeline(spec, base_dir=tmp_path)
    assert len(pipeline.loaders) == 2
    assert not (tmp_path / "data.db").exists()
