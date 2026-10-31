from etl_wore.pipeline.engine import Pipeline

class Source:
    def extract(self): yield {'nested':{'value':'original'}}
class MutatingSink:
    def load(self, rows):
        rows[0]['nested']['value'] = 'changed'
        rows.clear()
    def close(self): pass
class CapturingSink:
    def __init__(self): self.rows = []
    def load(self, rows): self.rows.extend(rows)
    def close(self): pass

def test_loader_mutations_cannot_change_other_destinations_or_metrics():
    capture = CapturingSink()
    context = (Pipeline('isolation').add_extractor(Source())
               .add_loader(MutatingSink()).add_loader(capture).run())
    assert capture.rows == [{'nested':{'value':'original'}}]
    assert context.records_loaded == 1
