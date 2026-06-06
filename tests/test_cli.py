from unittest.mock import patch

from inferdoctor.cli import main
from inferdoctor.core.models import CheckResult, Status


def _sample_result():
    return CheckResult(
        name="system",
        status=Status.PASS,
        summary="System information collected",
    )


@patch("inferdoctor.cli._results_for_target", return_value=[_sample_result()])
def test_check_command_renders_console(results, capsys):
    exit_code = main(["check", "system"])

    assert exit_code == 0
    assert "[PASS] system" in capsys.readouterr().out
    results.assert_called_once_with("system", None, None)


@patch("inferdoctor.cli._results_for_target", return_value=[_sample_result()])
def test_report_command_writes_json(results, tmp_path):
    output = tmp_path / "report.json"

    exit_code = main(["report", "--format", "json", "--output", str(output)])

    assert exit_code == 0
    assert '"name": "system"' in output.read_text(encoding="utf-8")
    results.assert_called_once_with(None, None, None)


@patch("inferdoctor.cli._results_for_target", return_value=[_sample_result()])
def test_check_timeout_and_verbose_options(results, capsys):
    exit_code = main(["check", "system", "--timeout", "4.5", "--verbose"])

    assert exit_code == 0
    assert "raw_data:" in capsys.readouterr().out
    results.assert_called_once_with("system", None, 4.5)


def test_timeout_must_be_positive(capsys):
    try:
        main(["check", "--timeout", "0"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected argparse to reject a zero timeout")

    assert "must be greater than zero" in capsys.readouterr().err
