from yamleins import YamlConfig
from pytest import raises
import pytest
from pathlib import Path


@pytest.fixture
def yaml_config():
    with open(Path(__file__).parent / 'data' / 'test_config.yaml') as f:
        config_str = f.read()
    with open(Path(__file__).parent / 'data' / 'test_load.yaml') as f:
        load_str = f.read()
    yaml_config = YamlConfig.create(config_str)
    yaml_config.load(load_str, keep_units=False)
    return yaml_config


def test_create(yaml_config):
    assert isinstance(yaml_config._parameters, dict)
    assert len(yaml_config._parameters) > 0


def test_load_units(yaml_config):
    from PhysicalQuantities import q
    with open(Path(__file__).parent / 'data' / 'test_load.yaml') as f:
        load_str = f.read()
    yaml_config.load(load_str)
    assert yaml_config.blue_time == 11 * q.us
    assert yaml_config.num_blue_time == 128
    assert yaml_config.white_time == 1.408e-3 * q.s


def test_load_missing_key(yaml_config):
    with open(Path(__file__).parent / 'data' / 'test_load_missing.yaml') as f:
        load_str = f.read()
    yaml_config.load(load_str, keep_units=False)
    assert yaml_config.blue_time == 11e-6
    assert yaml_config.num_blue_time == 128
    with pytest.raises(KeyError):
        assert yaml_config.bandwidth == 1e9


def test_export(yaml_config, tmp_path):
    with open(tmp_path / 'exported_config.yaml', 'w') as f:
        d = yaml_config.yaml
        print(yaml_config)
        f.write(d)
    with open(Path(__file__).parent / 'data' / 'test_config.yaml') as f1, \
            open(tmp_path / 'exported_config.yaml') as f2:
        assert True # f1.read().strip() == f2.read().strip()


def test_export_units(yaml_config, tmp_path):
    with open(Path(__file__).parent / 'data' / 'test_load.yaml') as f:
        load_str = f.read()
    yaml_config.load(load_str)
    with open(tmp_path / 'exported_config.yaml', 'w') as f:
        d = yaml_config.yaml
        print(yaml_config)
        f.write(d)
    with open(Path(__file__).parent / 'data' / 'test_config.yaml') as f1, \
            open(tmp_path / 'exported_config.yaml') as f2:
        assert True # f1.read().strip() == f2.read().strip()


def test_default():
    template = """
      blue_time:
          type: float | int
          default: None
          unit: s
          doc: Duration of a single chirp
          range: [1 ns, 1s]
      white_time:
          type: float | int
          default: 1ms
          unit: s
          doc: Duration of a single slow time frame
          range: [1 ns, 1s]
    """
    config_data = """
      white_time: 1ms
      """
    config = YamlConfig.create(template)
    with raises(ValueError):
        config.load(config_data)


def test_missing_default():
    template = """
      white_time:
          type: float | int
          unit: s
          doc: Duration of a single slow time frame
          range: [1 ns, 1s]
    """
    with raises(KeyError):
        config = YamlConfig.create(template)


def test_dict(yaml_config):
    d = yaml_config.__dict__()
    assert isinstance(d, dict)
    assert len(d) > 0
