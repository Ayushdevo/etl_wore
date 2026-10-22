from etl_wore.config import Config

def test_defaults_are_not_mutated():
    defaults = {"batch": 10}
    config = Config(defaults)
    config.set("batch", 20)
    assert defaults == {"batch": 10}
    defaults["batch"] = 30
    assert config.get("batch") == 20
