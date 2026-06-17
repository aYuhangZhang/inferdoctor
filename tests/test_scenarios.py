from inferdoctor.core.models import CheckResult, Status
from inferdoctor.core.scenarios import evaluate_scenarios, render_scenarios, scenario_names


def _result(name, status):
    return CheckResult(name=name, status=status, summary=f"{name} summary")


def test_scenario_names_include_initial_set():
    assert scenario_names() == [
        "local-chatbot",
        "rag-app",
        "openai-compatible-server",
        "dify-local-rag",
        "gpu-inference",
        "cpu-only-fallback",
    ]


def test_openai_server_fails_when_vllm_and_sglang_offline():
    scenarios = evaluate_scenarios(
        [
            _result("system", Status.PASS),
            _result("vllm", Status.SKIP),
            _result("sglang", Status.SKIP),
        ],
        "openai-compatible-server",
    )

    assert scenarios[0].status == Status.FAIL
    assert "OpenAI-compatible" in scenarios[0].reason


def test_gpu_inference_passes_with_nvidia_even_if_cuda_skips():
    scenarios = evaluate_scenarios(
        [
            _result("nvidia", Status.PASS),
            _result("cuda", Status.SKIP),
        ],
        "gpu-inference",
    )

    assert scenarios[0].status == Status.PASS
    assert "CUDA toolkit may be optional" in scenarios[0].reason


def test_render_scenarios_is_screenshot_friendly():
    output = render_scenarios(evaluate_scenarios([_result("system", Status.PASS)]))

    assert "InferDoctor Scenario Readiness" in output
    assert "Local chatbot:" in output
    assert "Status:" in output
    assert "Next step:" in output


def test_openai_server_passes_with_lmstudio():
    scenarios = evaluate_scenarios(
        [_result("lmstudio", Status.PASS)],
        "openai-compatible-server",
    )

    assert scenarios[0].status == Status.PASS
