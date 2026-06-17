from inferdoctor.core.explain import explain_topics, render_explanation


def test_explain_topics_include_initial_troubleshooting_set():
    topics = explain_topics()

    assert "openai-compatible-404" in topics
    assert "cuda-toolkit-missing" in topics
    assert "vllm-endpoint-not-reachable" in topics


def test_render_explanation_contains_required_sections():
    output = render_explanation("openai-compatible-404")

    assert "What it means:" in output
    assert "Common causes:" in output
    assert "What to try next:" in output
    assert "Related InferDoctor command:" in output
    assert "/v1/models" in output
