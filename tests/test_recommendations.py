from inferdoctor.core.recommendations import recommend_stack, render_recommendation


def test_recommend_stack_for_customer_service_with_24gib_vram():
    recommendation = recommend_stack(goal="customer-service", preference="easiest", vram_gib=24)

    assert recommendation.template == "customer-service"
    assert recommendation.runtime == "Ollama"
    assert "14B" in recommendation.model_size_class
    assert any("customer service" in item for item in recommendation.use_case_guidance)


def test_recommend_stack_for_local_api_performance():
    recommendation = recommend_stack(goal="local-api", preference="performance", vram_gib=24)

    assert recommendation.template == "openai-compatible-api"
    assert "vLLM" in recommendation.runtime
    rendered = render_recommendation(recommendation)
    assert "InferDoctor Stack Recommendation" in rendered
    assert "Use-case fit:" in rendered
    assert "OpenAI-compatible endpoint" in rendered
