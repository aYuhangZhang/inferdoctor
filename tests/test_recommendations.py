from inferdoctor.core.recommendations import recommend_stack, render_recommendation


def test_recommend_stack_for_customer_service_with_24gib_vram():
    recommendation = recommend_stack(goal="customer-service", preference="easiest", vram_gib=24)

    assert recommendation.template == "customer-service"
    assert recommendation.runtime == "Ollama"
    assert "14B" in recommendation.model_size_class


def test_recommend_stack_for_local_api_performance():
    recommendation = recommend_stack(goal="local-api", preference="performance", vram_gib=24)

    assert recommendation.template == "openai-compatible-api"
    assert "vLLM" in recommendation.runtime
    assert "InferDoctor Stack Recommendation" in render_recommendation(recommendation)
