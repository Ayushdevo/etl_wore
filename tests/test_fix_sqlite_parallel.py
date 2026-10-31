import sqlite3
from etl_wore.loaders.sqlite_loader import SqliteLoader
from etl_wore.pipeline.parallel import ParallelBatchLoader


def test_parallel_sqlite_batches_complete_and_close_from_main_thread(tmp_path):
    path = tmp_path / 'parallel.db'
    sink = SqliteLoader(str(path), 'records')
    parallel = ParallelBatchLoader(sink, max_workers=4)
    for i in range(40):
        parallel.load([{'id':i}])
    parallel.close()
    assert sink._conn is None
    with sqlite3.connect(path) as connection:
        values = [int(row[0]) for row in connection.execute('SELECT id FROM records')]
    assert sorted(values) == list(range(40))
