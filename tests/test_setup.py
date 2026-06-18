from inferdoctor.core.setup import recommend_setup, render_setup_plan


def test_recommend_setup_customer_service_easiest():
    plan = recommend_setup("customer-service", "easiest")

    assert plan.template == "customer-service"
    assert plan.recommended_runtime == "ollama"


def test_recommend_setup_document_qa_gpu():
    plan = recommend_setup("document-qa", "gpu")

    assert plan.template == "local-doc-qa"
    assert "vllm" in plan.recommended_runtime or "ollama" in plan.recommended_runtime
    assert "InferDoctor Guided Setup" in render_setup_plan(plan)
