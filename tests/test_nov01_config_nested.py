from etl_wore.config import Config


def test_nested_configuration_ownership():
    defaults = {"nested": {"values": [1]}}
    config = Config(defaults)
    defaults["nested"]["values"].append(2)
    assert config.get("nested") == {"values": [1]}
    config.get("nested")["values"].append(3)
    config.to_dict()["nested"]["values"].append(4)
    value = {"values": [5]}
    config.set("other", value)
    value["values"].append(6)
    assert config.get("nested") == {"values": [1]}
    assert config.get("other") == {"values": [5]}
