import json

from inferdoctor.core.checker import Checker
from inferdoctor.core.config import Config
from inferdoctor.core.models import CheckResult, Status
from inferdoctor.core.runner import run_checks
from inferdoctor.reporters import render_console, render_json, render_markdown


class BrokenChecker(Checker):
    name = "broken"

    def run(self, config):
        raise RuntimeError("boom")


def test_runner_contains_unexpected_checker_errors():
    result = run_checks([BrokenChecker()], Config())[0]

    assert result.status == Status.FAIL
    assert result.name == "broken"
    assert "RuntimeError" in result.details[0]


def test_reporters_render_structured_result():
    result = CheckResult(
        name="sample",
        status=Status.WARN,
        summary="Needs attention",
        details=["Detail"],
        suggestions=["Suggestion"],
        raw_data={"value": 1},
    )

    console = render_console([result])
    json_document = json.loads(render_json([result]))
    markdown = render_markdown([result])

    assert "[WARN] sample" in console
    assert json_document["results"][0]["raw_data"] == {"value": 1}
    assert "| sample | **WARN** | Needs attention |" in markdown


def test_verbose_reporters_include_raw_data():
    result = CheckResult(
        name="sample",
        status=Status.PASS,
        summary="Ready",
        raw_data={"timeout": 2.0},
    )

    assert '"timeout": 2.0' in render_console([result], verbose=True)
    assert "**Raw data**" in render_markdown([result], verbose=True)


def test_console_translations_zh():
    result = CheckResult(
        name="sample",
        status=Status.WARN,
        summary="需要注意",
        details=["详细信息"],
        suggestions=["建议"],
    )

    console = render_console([result], language="zh")

    assert "医生诊断" not in console  # console only renders result lines
    assert "建议：建议" in console


def test_console_translations_ja():
    result = CheckResult(
        name="sample",
        status=Status.WARN,
        summary="注意が必要です",
        details=["詳細"],
        suggestions=["提案"],
    )

    console = render_console([result], language="ja")

    assert "suggestion:" in console
    assert "提案" in console
