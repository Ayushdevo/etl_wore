import pytest

from etl_wore.exceptions import ExtractionError
from etl_wore.pipeline.engine import Pipeline


class Source:
    def extract(self):
        yield [("id", 1)]


class Sink:
    def __init__(self):
        self.rows = []
        self.closed = False

    def load(self, rows):
        self.rows.extend(rows)

    def close(self):
        self.closed = True


def test_invalid_source_does_not_reach_sink():
    sink = Sink()
    with pytest.raises(ExtractionError, match="object"):
        Pipeline("shape").add_extractor(Source()).add_loader(sink).run()
    assert sink.rows == [] and sink.closed
