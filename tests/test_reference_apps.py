from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUSTOMER_SERVICE = ROOT / "examples" / "reference_apps" / "customer_service"


def _run(app_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "app.py", *args],
        cwd=app_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5,
        check=False,
    )


def test_customer_service_reference_app_safe_modes():
    help_result = _run(CUSTOMER_SERVICE, "--help")
    assert help_result.returncode == 0
    assert "--dry-run" in help_result.stdout

    config_result = _run(CUSTOMER_SERVICE, "--check-config")
    assert config_result.returncode == 0
    assert "Endpoint:" in config_result.stdout
    assert "No endpoint call was made." in config_result.stdout

    dry_result = _run(CUSTOMER_SERVICE, "--dry-run")
    assert dry_result.returncode == 0
    assert "Dry run" in dry_result.stdout
    assert "No endpoint call was made." in dry_result.stdout


def test_customer_service_reference_app_docs_include_performance_loop():
    readme = (CUSTOMER_SERVICE / "README.md").read_text(encoding="utf-8")
    config = (CUSTOMER_SERVICE / "config.yaml").read_text(encoding="utf-8")
    env_example = (CUSTOMER_SERVICE / ".env.example").read_text(encoding="utf-8")

    assert "inferdoctor perf baseline create" in readme
    assert "inferdoctor perf compare before.json after.json" in readme
    assert "inferdoctor optimize plan" in readme
    assert "--allow-non-local" in readme
    assert "streaming: true" in config
    assert "LOCAL_AI_STREAMING=true" in env_example
