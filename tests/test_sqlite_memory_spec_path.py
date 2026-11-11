from etl_wore.builder import build_pipeline
def test_memory_database_is_not_resolved_to_a_disk_filename(tmp_path):
    spec = {'name': 'memory', 'extractors': [{'type': 'json', 'filepath': 'input.json'}], 'loaders': [{'type': 'sqlite', 'db_path': ':memory:', 'table_name': 'rows'}]}
    loader = build_pipeline(spec, base_dir=tmp_path).loaders[0]
    assert loader.db_path == ':memory:'
    loader.load([{'id': 1}])
    loader.close()
    assert list(tmp_path.iterdir()) == []
