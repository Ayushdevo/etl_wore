import pytest

from etl_wore.exceptions import TransformationError
from etl_wore.pipeline.engine import Pipeline


class Source:
    def extract(self):
        yield {"id": 1}


class Transform:
    def transform(self, record):
        return []


class Sink:
    def load(self, rows):
        raise AssertionError("invalid rows reached sink")

    def close(self):
        pass


def test_invalid_transformation_is_reported():
    with pytest.raises(TransformationError, match="object"):
        Pipeline("shape").add_extractor(Source()).add_transformer(
            Transform()
        ).add_loader(Sink()).run()
