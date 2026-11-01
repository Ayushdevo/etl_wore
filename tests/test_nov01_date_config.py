import pytest

from etl_wore.transformers.date_normalizer import DateNormalizer


@pytest.mark.parametrize("fields", ["date", [], [1], [""]])
def test_invalid_date_fields_fail_early(fields):
    with pytest.raises(ValueError):
        DateNormalizer(fields)


def test_config_cannot_change_after_construction():
    fields = ["date"]
    normalizer = DateNormalizer(fields)
    fields.clear()
    assert (
        normalizer.transform({"date": "2026-01-01"})["date"] == "2026-01-01T00:00:00Z"
    )


def test_invalid_output_format():
    with pytest.raises(ValueError):
        DateNormalizer(["date"], output_format=None)
