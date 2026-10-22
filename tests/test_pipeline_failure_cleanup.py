from unittest.mock import Mock
import pytest
from etl_wore.pipeline.engine import Pipeline

@pytest.mark.parametrize("failure", ["extract", "load", "close"])
def test_all_loaders_close_on_failure(failure):
    first, second = Mock(), Mock()
    extractor = Mock()
    extractor.extract.return_value = iter([{"id":1}])
    if failure == "extract":
        extractor.extract.side_effect = ValueError("processing")
    elif failure == "load":
        first.load.side_effect = ValueError("processing")
    first.close.side_effect = RuntimeError("closing")
    pipeline = Pipeline("test").add_extractor(extractor).add_loader(first).add_loader(second)
    error = RuntimeError if failure == "close" else ValueError
    with pytest.raises(error):
        pipeline.run()
    first.close.assert_called_once()
    second.close.assert_called_once()
