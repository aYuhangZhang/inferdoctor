from unittest.mock import patch

import pytest

from inferdoctor.cli import _results_for_target, main
from inferdoctor.core.config import Config
from inferdoctor.core.models import CheckResult, Status


def _sample_result():
    return CheckResult(
        name="system",
        status=Status.PASS,
        summary="System information collected",
    )


def _sample_run():
    return [_sample_result()], Config()


@patch("inferdoctor.cli._results_for_target", return_value=_sample_run())
def test_default_command_renders_health_dashboard(results, capsys):
    exit_code = main([])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "InferDoctor - Local AI Stack Health Check" in output
    assert "Overall Health: 100 / 100" in output
    results.assert_called_once_with(None, None, None, None)


@patch("inferdoctor.cli._results_for_target", return_value=_sample_run())
def test_check_command_renders_dashboard(results, capsys):
    exit_code = main(["check", "system"])

    assert exit_code == 0
    assert "System      PASS" in capsys.readouterr().out
    results.assert_called_once_with("system", None, None, None)


@patch("inferdoctor.cli._results_for_target", return_value=_sample_run())
def test_report_command_writes_json(results, tmp_path):
    output = tmp_path / "report.json"

    exit_code = main(["report", "--format", "json", "--output", str(output)])

    assert exit_code == 0
    assert '"name": "system"' in output.read_text(encoding="utf-8")
    results.assert_called_once_with(None, None, None, None)


@patch("inferdoctor.cli._results_for_target", return_value=_sample_run())
def test_check_timeout_verbose_and_endpoint_options(results, capsys):
    endpoint = "http://127.0.0.1:30000/v1"
    exit_code = main(
        ["check", "sglang", "--timeout", "4.5", "--endpoint", endpoint, "--verbose"]
    )

    assert exit_code == 0
    assert "Detailed diagnostics:" in capsys.readouterr().out
    results.assert_called_once_with("sglang", None, 4.5, endpoint)


def test_endpoint_requires_http_checker():
    with pytest.raises(SystemExit, match="does not use an HTTP endpoint"):
        _results_for_target("system", None, endpoint="http://127.0.0.1:1")


def test_timeout_must_be_positive(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["check", "--timeout", "0"])

    assert exc.value.code == 2
    assert "must be greater than zero" in capsys.readouterr().err


def test_endpoint_override_rejects_invalid_url():
    with pytest.raises(SystemExit, match="http:// or https://"):
        _results_for_target("sglang", None, endpoint="127.0.0.1:30000/v1")


@patch("inferdoctor.cli._results_for_target")
def test_explain_command_does_not_run_checks(results, capsys):
    exit_code = main(["explain", "cuda-toolkit-missing"])

    assert exit_code == 0
    assert "InferDoctor Explain:" in capsys.readouterr().out
    results.assert_not_called()


@patch("inferdoctor.cli._results_for_target")
def test_capacity_command_does_not_run_checks(results, capsys):
    exit_code = main(["capacity", "--vram", "24"])

    assert exit_code == 0
    assert "InferDoctor Capacity Preview" in capsys.readouterr().out
    results.assert_not_called()


@patch("inferdoctor.cli._results_for_target", return_value=_sample_run())
def test_scenario_command_renders_readiness(results, capsys):
    exit_code = main(["scenario"])

    assert exit_code == 0
    assert "InferDoctor Scenario Readiness" in capsys.readouterr().out
    results.assert_called_once_with(None, None, None, None)


@patch("inferdoctor.cli._results_for_target", return_value=_sample_run())
def test_scenarios_alias_renders_readiness(results, capsys):
    exit_code = main(["scenarios", "cpu-only-fallback"])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert "CPU-only fallback:" in output
    assert "Local chatbot:" not in output
