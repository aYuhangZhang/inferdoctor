import json

from inferdoctor.core.config import Config
from inferdoctor.core.models import CheckResult, Status
from inferdoctor.core.profile import build_profile, redact_value, render_profile_markdown


def _results():
    return [
        CheckResult(
            name="system",
            status=Status.PASS,
            summary="System information collected",
            raw_data={
                "os": "Linux-test",
                "python_version": "3.12.0",
                "python_executable": "/home/user/project/.venv/bin/python",
                "architecture": "x86_64",
                "available_memory_bytes": 8 * 1024 ** 3,
            },
        ),
        CheckResult(
            name="nvidia",
            status=Status.PASS,
            summary="1 NVIDIA GPU(s) detected",
            raw_data={
                "nvidia_smi_path": "/usr/bin/nvidia-smi",
                "gpus": [
                    {
                        "name": "NVIDIA RTX 4090",
                        "memory_total_mib": 24564,
                        "driver_version": "550.54.14",
                    }
                ],
            },
        ),
        CheckResult(
            name="ollama",
            status=Status.SKIP,
            summary="Ollama was not found and its API is not reachable",
            raw_data={"ollama_path": None},
        ),
    ]


def test_redact_value_hides_sensitive_keys_and_home_paths():
    assert redact_value("abc", "api_key") == "<redacted>"
    assert redact_value("/home/alice/.venv/bin/python") == "~/.../python"
    assert (
        redact_value("http://user:pass@127.0.0.1:8000/v1?token=abc")
        == "http://127.0.0.1:8000/v1?<redacted>"
    )


def test_build_profile_contains_safe_summary():
    config = Config(endpoints={"ollama": "http://user:pass@127.0.0.1:11434?token=abc"})

    profile = build_profile(_results(), config)

    assert profile["safe_to_share"] is True
    assert profile["system"]["available_memory_gib"] == 8.0
    assert profile["gpus"][0]["memory_total_gib"] == 24.0
    assert profile["commands"]["nvidia-smi"]["available"] is True
    assert profile["configured_endpoints"]["ollama"] == "http://127.0.0.1:11434?<redacted>"
    assert profile["checker_summary"][0] == {
        "name": "system",
        "status": "pass",
        "summary": "System information collected",
    }


def test_render_profile_markdown_is_shareable():
    markdown = render_profile_markdown(_results(), Config())

    assert "# InferDoctor Safe Diagnostic Profile" in markdown
    assert "## Top Fixes" in markdown
    assert "/home/" not in markdown
    assert "NVIDIA RTX 4090" in markdown


def test_profile_json_is_serializable():
    json.dumps(build_profile(_results(), Config()))
