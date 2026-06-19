import pytest
from config import AppConfig, load_config, create_default_config


@pytest.fixture
def temp_config_file(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir / "config.ini"


@pytest.fixture
def valid_config_file(temp_config_file):
    content = """
[spotify]
client_id = test_client_id
client_secret = test_client_secret
redirect_uri = http://localhost:8888/callback

[ai]
provider = anthropic
api_key = test_api_key
model = claude-3-haiku
"""
    temp_config_file.write_text(content)
    return temp_config_file


def test_load_config_with_valid_file(valid_config_file, monkeypatch):
    monkeypatch.setattr("config.CONFIG_FILE", valid_config_file)
    config = load_config()
    assert isinstance(config, AppConfig)
    assert config.spotify.client_id == "test_client_id"
    assert config.ai.provider == "anthropic"


def test_create_default_config(temp_config_file, monkeypatch):
    monkeypatch.setattr("config.CONFIG_FILE", temp_config_file)
    create_default_config()
    assert temp_config_file.exists()
