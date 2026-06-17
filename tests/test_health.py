from inferdoctor.core.config import Config
from inferdoctor.core.health import calculate_health, recommend_fixes
from inferdoctor.core.models import CheckResult, Status
from inferdoctor.reporters.console import render_dashboard


def _result(name, status, summary=None):
    return CheckResult(
        name=name,
        status=status,
        summary=summary or "{0} result".format(name),
    )


def test_health_score_uses_transparent_status_weights():
    health = calculate_health(
        [
            _result("system", Status.PASS),
            _result("vllm", Status.WARN),
            _result("sglang", Status.FAIL),
            _result("dify", Status.SKIP),
        ]
    )

    assert health.score == 61
    assert health.label == "Needs attention"


def test_recommendations_prioritize_fail_then_warn_then_skip():
    fixes = recommend_fixes(
        [
            _result("ollama", Status.SKIP),
            _result("vllm", Status.WARN),
            _result("sglang", Status.FAIL),
            _result("dify", Status.SKIP),
        ],
        Config(),
    )

    assert [fix.component for fix in fixes] == ["SGLang", "vLLM", "Ollama"]
    assert fixes[0].next_command.startswith("inferdoctor check sglang")


def test_dashboard_contains_title_table_score_and_top_fixes():
    output = render_dashboard(
        [
            _result("system", Status.PASS, "System information collected"),
            _result("sglang", Status.SKIP, "SGLang endpoint is not reachable"),
        ],
        Config(),
    )

    assert "InferDoctor - Local AI Stack Health Check" in output
    assert "Overall Health:" in output
    assert "Stack Summary:" in output
    assert "Doctor's read:" in output
    assert "SGLang      SKIP" in output
    assert "Top recommended fixes (most useful first):" in output
    assert "Likely cause:" in output
    assert "Impact:" in output


def test_all_warn_and_fail_results_receive_actions_beyond_default_limit():
    results = [
        _result("vllm", Status.WARN),
        _result("sglang", Status.WARN),
        _result("ollama", Status.FAIL),
        _result("dify", Status.WARN),
    ]

    assert len(recommend_fixes(results, Config())) == 4


def test_404_fix_uses_checker_suggested_endpoint():
    result = CheckResult(
        name="vllm",
        status=Status.WARN,
        summary="vLLM models route returned HTTP 404",
        suggestions=[
            "Try: inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1"
        ],
    )
    config = Config()
    config.endpoints["vllm"] = "http://127.0.0.1:8000"

    fix = recommend_fixes([result], config)[0]

    assert fix.next_command.endswith("http://127.0.0.1:8000/v1")
    assert fix.config_hint.endswith("http://127.0.0.1:8000/v1")


def test_cuda_fix_mentions_driver_available_when_nvidia_passes():
    fixes = recommend_fixes(
        [
            _result("nvidia", Status.PASS, "1 NVIDIA GPU(s) detected"),
            _result("cuda", Status.SKIP, "CUDA compiler was not found"),
        ],
        Config(),
    )

    assert fixes[0].component == "CUDA"
    assert "NVIDIA driver is available" in fixes[0].likely_cause
    assert "Optional" in fixes[0].impact


def test_dify_fix_marks_service_optional():
    fixes = recommend_fixes(
        [_result("dify", Status.SKIP, "Dify endpoint is not reachable")],
        Config(),
    )

    assert fixes[0].component == "Dify"
    assert "Dify is optional" in fixes[0].likely_cause
    assert "Optional unless Dify" in fixes[0].impact
