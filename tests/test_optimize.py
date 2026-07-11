from inferdoctor.core.optimize import advise_endpoint, advise_rag, render_optimization_report


def test_optimize_endpoint_advice_for_vllm():
    report = advise_endpoint(runtime="vllm", vram_gib=24, model_size="14b", quant="q4")
    rendered = render_optimization_report(report)

    assert "Endpoint UX Optimization Advice" in rendered
    assert "vLLM" in rendered or "vllm" in rendered
    assert "streaming" in rendered.lower()
    assert "inferdoctor perf endpoint" in rendered


def test_optimize_endpoint_advice_with_metrics():
    report = advise_endpoint(runtime="ollama", streaming=True, ttft=1.5, tps=40, latency=3.2)
    rendered = render_optimization_report(report)

    assert "Ollama" in rendered or "ollama" in rendered
    assert "Observed TTFT: 1.5s" in rendered
    assert "benchmark" in rendered


def test_optimize_rag_advice_for_high_top_k():
    report = advise_rag(docs=1000, chunks=5000, top_k=8, ttft=2.5, streaming=True)
    rendered = render_optimization_report(report)

    assert "RAG UX Optimization Advice" in rendered
    assert "top_k is high" in rendered
    assert "context budget" in rendered.lower() or "prompt size" in rendered.lower()


def test_optimize_rag_advice_for_rerank_latency():
    report = advise_rag(retrieval_ms=900, rerank_ms=1500, top_k=12)
    rendered = render_optimization_report(report)

    assert "Retrieval latency" in rendered
    assert "Reranking" in rendered
    assert "top_k=4" in rendered
