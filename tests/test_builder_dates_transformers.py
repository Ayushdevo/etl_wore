from etl_wore.builder import _component, _TRANSFORMERS


def test_date_stage_normalizes_offsets_before_output():
    stage = _component({"type": "dates", "date_fields": ["created"]}, _TRANSFORMERS, "stage")
    assert stage.transform({"created": "2026-10-30T10:00:00+05:30"}) == {"created": "2026-10-30T04:30:00Z"}
    assert stage.transform({"created": "unparseable"}) == {"created": "unparseable"}
