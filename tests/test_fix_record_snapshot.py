from etl_wore.pipeline.engine import Pipeline

class ReusingSource:
    def extract(self):
        record = {'nested':{'value':0}}
        for value in range(3):
            record['nested']['value'] = value
            yield record

class Sink:
    def __init__(self): self.rows = []
    def load(self, rows): self.rows.extend(rows)
    def close(self): pass

def test_generator_can_reuse_a_mutable_record_buffer():
    sink = Sink()
    Pipeline('snapshot', batch_size=3).add_extractor(ReusingSource()).add_loader(sink).run()
    assert [row['nested']['value'] for row in sink.rows] == [0, 1, 2]
