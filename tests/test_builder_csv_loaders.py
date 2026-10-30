import csv
from etl_wore.builder import _component, _LOADERS


def test_csv_sink_reuses_headers_across_batches(tmp_path):
    path = tmp_path / "nested" / "out.csv"
    sink = _component({"type": "csv", "output_path": str(path), "delimiter": ";"}, _LOADERS, "sink")
    sink.load([{"id": 1, "name": "café"}])
    sink.load([{"name": "Jane; Doe", "id": 2}])
    sink.close()
    with path.open(newline="", encoding="utf-8") as file:
        assert list(csv.DictReader(file, delimiter=";")) == [{"id": "1", "name": "café"}, {"id": "2", "name": "Jane; Doe"}]
