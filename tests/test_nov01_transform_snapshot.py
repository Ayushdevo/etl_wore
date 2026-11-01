from etl_wore.pipeline.engine import Pipeline


class Source:
    def extract(self):
        yield {"id": 1}
        yield {"id": 2}


class Transform:
    def __init__(self):
        self.buffer = {}

    def transform(self, record):
        self.buffer.update(record)
        return self.buffer


class Sink:
    def load(self, rows):
        self.rows = rows

    def close(self):
        pass


def test_reused_transform_buffer_does_not_overwrite_previous_rows():
    sink = Sink()
    Pipeline("snapshot").add_extractor(Source()).add_transformer(
        Transform()
    ).add_loader(sink).run()
    assert sink.rows == [{"id": 1}, {"id": 2}]
