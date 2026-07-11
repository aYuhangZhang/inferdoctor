from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class OptimizationReport:
    title: str
    situation: List[str] = field(default_factory=list)
    bottlenecks: List[str] = field(default_factory=list)
    quick_wins: List[str] = field(default_factory=list)
    next_commands: List[str] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)


def _model_size_number(model_size: Optional[str]) -> Optional[float]:
    if not model_size:
        return None
    text = model_size.strip().lower()
    if text.endswith("b"):
        text = text[:-1]
    try:
        return float(text)
    except ValueError:
        return None


def _fmt(value: Optional[float], unit: str = "") -> str:
    if value is None:
        return "not provided"
    return "{0:g}{1}".format(value, unit)


def advise_endpoint(
    runtime: Optional[str] = None,
    vram_gib: Optional[float] = None,
    model_size: Optional[str] = None,
    quant: Optional[str] = None,
    streaming: bool = False,
    ttft: Optional[float] = None,
    tps: Optional[float] = None,
    latency: Optional[float] = None,
) -> OptimizationReport:
    runtime_label = runtime or "openai-compatible"
    size_b = _model_size_number(model_size)
    situation = [
        "Runtime: {0}".format(runtime_label),
        "VRAM: {0}".format(_fmt(vram_gib, " GiB")),
        "Model size: {0}".format(model_size or "not provided"),
        "Quantization: {0}".format(quant or "not provided"),
        "Streaming: {0}".format("enabled" if streaming else "not provided / possibly disabled"),
        "Observed TTFT: {0}".format(_fmt(ttft, "s")),
        "Observed TPS: {0}".format(_fmt(tps, " tok/s")),
        "Observed total latency: {0}".format(_fmt(latency, "s")),
    ]
    bottlenecks: List[str] = []
    quick_wins: List[str] = []

    if not streaming:
        bottlenecks.append("Perceived latency may be high because streaming is not confirmed.")
        quick_wins.append("Enable streaming in the app UI so users see the first token quickly.")
    if ttft is not None and ttft > 2.0:
        bottlenecks.append("TTFT is above 2s, which can feel slow in interactive demos.")
        quick_wins.append("Warm up the endpoint before demos and keep the model loaded if the runtime supports it.")
        quick_wins.append("Reduce prompt/context size before generation; long context often hurts TTFT.")
    if latency is not None and latency > 8.0:
        bottlenecks.append("Total latency is high for a customer-facing prototype.")
        quick_wins.append("Use shorter responses, smaller context, or a smaller/quantized model for interactive flows.")
    if tps is not None and tps < 20:
        bottlenecks.append("Output speed is low; long answers will feel slow even with streaming.")
        quick_wins.append("Prefer shorter answer style or a smaller model for chat-heavy workflows.")
    if size_b and vram_gib:
        if size_b >= 32 and vram_gib <= 24:
            bottlenecks.append("A 32B-class model on 24 GiB or less VRAM may be tight for interactive serving.")
            quick_wins.append("Try a 7B/8B or 14B quantized model for customer demos before optimizing larger models.")
        elif size_b >= 14 and vram_gib < 16:
            bottlenecks.append("A 14B-class model may be oversized for this VRAM budget.")
            quick_wins.append("Use q4 quantization or a smaller model size class for lower TTFT.")
    if runtime_label == "ollama":
        quick_wins.append("Ollama is a good easiest-path runtime; use streaming clients and run a warm-up prompt before demos.")
    elif runtime_label == "vllm":
        quick_wins.append("For vLLM, verify the base URL ends with /v1 and tune max model length / batching for your workload.")
    elif runtime_label == "sglang":
        quick_wins.append("For SGLang, verify /v1 routing and keep prompts concise while validating latency.")
    elif runtime_label == "openai-compatible":
        quick_wins.append("Run inferdoctor perf streaming against the endpoint to check whether stream=true is actually supported.")

    if not bottlenecks:
        bottlenecks.append("No obvious bottleneck from the supplied metrics; run a lightweight perf smoke test for more signal.")
    if not quick_wins:
        quick_wins.append("Collect TTFT, total latency, and rough TPS with inferdoctor perf before tuning.")

    next_commands = [
        "inferdoctor perf endpoint --endpoint http://127.0.0.1:8000/v1 --model local-model",
        "inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model",
        "inferdoctor model fit --size {0} --quant {1} --vram {2}".format(model_size or "14b", quant or "q4", _fmt(vram_gib) if vram_gib is not None else "24"),
    ]
    caveats = [
        "This advice is heuristic and based only on supplied metrics; it is not a benchmark.",
        "InferDoctor cannot see model architecture, KV cache settings, context length, batching, or GPU utilization from this command alone.",
    ]
    return OptimizationReport("Endpoint UX Optimization Advice", situation, bottlenecks, quick_wins, next_commands, caveats)


def advise_rag(
    docs: Optional[int] = None,
    chunks: Optional[int] = None,
    top_k: Optional[int] = None,
    rerank: bool = False,
    retrieval_ms: Optional[float] = None,
    rerank_ms: Optional[float] = None,
    ttft: Optional[float] = None,
    streaming: bool = False,
    model_size: Optional[str] = None,
    vram_gib: Optional[float] = None,
) -> OptimizationReport:
    situation = [
        "Documents: {0}".format(docs if docs is not None else "not provided"),
        "Chunks: {0}".format(chunks if chunks is not None else "not provided"),
        "top_k: {0}".format(top_k if top_k is not None else "not provided"),
        "Rerank: {0}".format("enabled" if rerank else "not provided / disabled"),
        "Retrieval latency: {0}".format(_fmt(retrieval_ms, "ms")),
        "Rerank latency: {0}".format(_fmt(rerank_ms, "ms")),
        "Observed TTFT: {0}".format(_fmt(ttft, "s")),
        "Streaming: {0}".format("enabled" if streaming else "not provided / possibly disabled"),
        "Model size: {0}".format(model_size or "not provided"),
        "VRAM: {0}".format(_fmt(vram_gib, " GiB")),
    ]
    bottlenecks: List[str] = []
    quick_wins: List[str] = []

    if not streaming:
        bottlenecks.append("Users may see a blank wait during retrieval and generation.")
        quick_wins.append("Enable SSE/streaming and show retrieval progress before generation starts.")
    if retrieval_ms is not None and retrieval_ms > 500:
        bottlenecks.append("Retrieval latency is noticeable before generation begins.")
        quick_wins.append("Cache embeddings, pre-load the index, and show a 'searching documents' progress event.")
    if rerank or (rerank_ms is not None and rerank_ms > 0):
        if rerank_ms is not None and rerank_ms > 800:
            bottlenecks.append("Reranking is adding significant pre-generation delay.")
        quick_wins.append("Use rerank only when quality requires it, or rerank fewer candidates for interactive demos.")
    if top_k is not None and top_k > 6:
        bottlenecks.append("top_k is high; too many chunks can inflate prompt size and hurt TTFT.")
        quick_wins.append("Start with top_k=4 or top_k=5, then increase only if answer quality needs it.")
    if chunks is not None and chunks > 3000:
        bottlenecks.append("Large chunk counts can slow retrieval if the index is not optimized or cached.")
        quick_wins.append("Check chunking quality and cache the index before demos.")
    if ttft is not None and ttft > 2.0:
        bottlenecks.append("Generation TTFT is high after retrieval.")
        quick_wins.append("Reduce context budget and prompt size; warm up the endpoint before the first customer question.")
    if model_size and vram_gib:
        size_b = _model_size_number(model_size)
        if size_b and size_b >= 14 and vram_gib < 16:
            bottlenecks.append("The generation model may be large for the available VRAM.")
            quick_wins.append("Use a smaller or more aggressively quantized model for interactive RAG demos.")

    if not bottlenecks:
        bottlenecks.append("No obvious RAG bottleneck from supplied metrics; measure retrieval and generation separately.")
    if not quick_wins:
        quick_wins.append("Add timestamps around retrieval, rerank, prompt assembly, TTFT, and total answer latency.")

    next_commands = [
        "inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model",
        "inferdoctor optimize endpoint --streaming --ttft {0}".format(_fmt(ttft) if ttft is not None else "2.5"),
        "inferdoctor template create local-doc-qa --output ./local-doc-qa-demo",
    ]
    caveats = [
        "This command does not run retrieval, embeddings, rerankers, or model inference.",
        "RAG UX depends on corpus shape, chunking, index type, reranker, prompt budget, model runtime, and UI progress events.",
    ]
    return OptimizationReport("RAG UX Optimization Advice", situation, bottlenecks, quick_wins, next_commands, caveats)


def render_optimization_report(report: OptimizationReport) -> str:
    lines = [report.title, "=" * 57, "Current situation:"]
    lines.extend("- {0}".format(item) for item in report.situation)
    lines.extend(["", "Likely bottlenecks:"])
    lines.extend("- {0}".format(item) for item in report.bottlenecks)
    lines.extend(["", "Recommended quick wins:"])
    lines.extend("{0}. {1}".format(index, item) for index, item in enumerate(report.quick_wins, start=1))
    lines.extend(["", "Safe next commands:"])
    lines.extend("- {0}".format(item) for item in report.next_commands)
    lines.extend(["", "What InferDoctor cannot know yet:"])
    lines.extend("- {0}".format(item) for item in report.caveats)
    return "\n".join(lines)
