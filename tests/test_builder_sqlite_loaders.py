import sqlite3
from etl_wore.builder import build_pipeline


def test_sqlite_sink_runs_and_releases_database(tmp_path):
    source = tmp_path / "records.csv"
    target = tmp_path / "out.db"
    source.write_text('id,name\n1,Ada\n2,Grace\n')
    spec = {"name": "load", "batch_size": 1, "extractors": [{"type": "csv", "filepath": str(source)}], "loaders": [{"type": "sqlite", "db_path": str(target), "table_name": 'order "details"'}]}
    pipeline = build_pipeline(spec)
    pipeline.run()
    assert pipeline.loaders[0]._conn is None
    with sqlite3.connect(target) as conn:
        assert conn.execute('SELECT * FROM "order ""details"""').fetchall() == [("1", "Ada"), ("2", "Grace")]
