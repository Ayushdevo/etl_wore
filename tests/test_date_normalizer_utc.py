from etl_wore.transformers.date_normalizer import DateNormalizer

def test_timezone_offset_is_converted_before_utc_suffix():
    normalizer = DateNormalizer(["time"])
    original = {"time": "2026-10-22T10:00:00+05:30"}
    assert normalizer.transform(original)["time"] == "2026-10-22T04:30:00Z"
    assert original["time"].endswith("+05:30")
    assert normalizer.transform({"time": "2026-10-22T10:00:00"})["time"] == "2026-10-22T10:00:00Z"
