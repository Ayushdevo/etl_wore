import pytest
from etl_wore.pipeline.engine import Pipeline
from etl_wore.extractors.base import BaseExtractor
from etl_wore.loaders.base import BaseLoader


class Source(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.closed = False
        self.iterator = self.records()
    def records(self):
        try:
            yield {"id": 1}
            yield {"id": 2}
        finally:
            self.closed = True
    def extract(self):
        return self.iterator


class FailingSink(BaseLoader):
    def __init__(self):
        super().__init__()
        self.closed = False
    def load(self, records):
        raise RuntimeError("destination failure")
    def close(self):
        self.closed = True


def test_failed_batch_closes_a_retained_extractor_iterator():
    source, sink = Source(), FailingSink()
    pipeline = Pipeline("cleanup", batch_size=1).add_extractor(source).add_loader(sink)
    with pytest.raises(RuntimeError, match="destination failure"):
        pipeline.run()
    assert source.closed
    assert sink.closed


def test_iterator_cleanup_does_not_hide_processing_error():
    class BrokenIterator:
        def __iter__(self): return self
        def __next__(self): return {"id": 1}
        def close(self): raise ValueError("cleanup failure")
    class BrokenSource(BaseExtractor):
        def extract(self): return BrokenIterator()
    sink = FailingSink()
    with pytest.raises(RuntimeError, match="destination failure"):
        Pipeline("cleanup", batch_size=1).add_extractor(BrokenSource()).add_loader(sink).run()
    assert sink.closed
