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



def test_optimize_endpoint_advice_is_evidence_structured():
    report = advise_endpoint(
        runtime="vllm",
        vram_gib=24,
        model_size="32b",
        quant="q4",
        streaming=False,
        ttft=3.2,
        latency=9.0,
        context_tokens=12000,
        ttft_variance=2.5,
        docker=True,
        cold_start=True,
    )
    rendered = render_optimization_report(report)

    assert "Observation:" in rendered
    assert "Impact:" in rendered
    assert "Action:" in rendered
    assert "Next:" in rendered
    assert "Limitation:" in rendered
    assert "TTFT is above 2 seconds" in rendered
    assert "Context size is large" in rendered
    assert "Docker" in rendered
    assert len(report.quick_wins) <= 5


def test_optimize_endpoint_cpu_fallback_advice():
    rendered = render_optimization_report(advise_endpoint(cpu_fallback_suspected=True))

    assert "CPU fallback" in rendered
    assert "inferdoctor check nvidia" in rendered
