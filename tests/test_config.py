import json

import pytest

from inferdoctor.core.config import ConfigError, load_config


def test_load_simple_yaml_config(tmp_path):
    path = tmp_path / "inferdoctor.yaml"
    path.write_text(
        "\n".join(
            [
                "endpoints:",
                "  ollama: http://ollama.local:11434",
                "  vllm: http://vllm.local:8000/v1/",
                "timeout: 3.5",
            ]
        ),
        encoding="utf-8",
    )

    config = load_config(str(path))

    assert config.endpoints["ollama"] == "http://ollama.local:11434"
    assert config.endpoints["vllm"] == "http://vllm.local:8000/v1"
    assert config.endpoints["xinference"] == "http://127.0.0.1:9997"
    assert config.timeout == 3.5


def test_load_json_config(tmp_path):
    path = tmp_path / "inferdoctor.json"
    path.write_text(
        json.dumps({"endpoints": {"dify": "http://dify.local"}}),
        encoding="utf-8",
    )

    assert load_config(str(path)).endpoints["dify"] == "http://dify.local"


def test_unknown_endpoint_is_rejected(tmp_path):
    path = tmp_path / "inferdoctor.yaml"
    path.write_text("endpoints:\n  unknown: http://localhost\n", encoding="utf-8")

    with pytest.raises(ConfigError, match="Unknown endpoint"):
        load_config(str(path))
