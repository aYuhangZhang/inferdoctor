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
    context_tokens: Optional[int] = None,
    ttft_variance: Optional[float] = None,
    containerized: bool = False,
    docker: bool = False,
    cold_start: bool = False,
    cpu_fallback_suspected: bool = False,
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
        "Context tokens: {0}".format(context_tokens if context_tokens is not None else "not provided"),
        "TTFT variance: {0}".format(_fmt(ttft_variance, "x")),
        "Containerized: {0}".format("yes" if containerized else "not provided / no"),
        "Docker involved: {0}".format("yes" if docker else "not provided / no"),
        "Cold start observed: {0}".format("yes" if cold_start else "not provided / no"),
        "CPU fallback suspected: {0}".format("yes" if cpu_fallback_suspected else "not provided / no"),
    ]
    bottlenecks: List[str] = []
    recommendations: List[tuple[int, str]] = []

    def add(priority: int, observation: str, impact: str, action: str, next_command: str, limitation: str) -> None:
        bottlenecks.append(observation)
        recommendations.append(
            (
                priority,
                "Observation: {0}\nImpact: {1}\nAction: {2}\nNext: {3}\nLimitation: {4}".format(
                    observation,
                    impact,
                    action,
                    next_command,
                    limitation,
                ),
            )
        )

    if not streaming:
        add(
            10,
            "Streaming is not confirmed.",
            "Users may stare at a blank UI while the model is working.",
            "Enable streaming in the app and validate stream=true before a demo.",
            "inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model",
            "InferDoctor does not know whether your frontend actually renders chunks as they arrive.",
        )
    if ttft is not None and ttft > 2.0:
        add(
            20,
            "TTFT is above 2 seconds.",
            "The first answer can feel slow even if generation speed is good.",
            "Warm up the endpoint, reduce context length, and check whether the model is too large for the hardware.",
            "inferdoctor optimize endpoint --streaming --ttft {0:g}".format(ttft),
            "TTFT depends on runtime cache state, model loading, context size, and network path.",
        )
    if cold_start:
        add(
            25,
            "Cold-start behavior was observed.",
            "The first user or customer question may be much slower than later turns.",
            "Run one harmless warmup prompt before demos and keep the model loaded if the runtime supports it.",
            "inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model --warmup 1 --runs 2",
            "Warmup does not fix undersized hardware or oversized context.",
        )
    if ttft_variance is not None and ttft_variance >= 2.0:
        add(
            30,
            "TTFT varied by 2x or more across runs.",
            "The app may feel unstable even when the median looks acceptable.",
            "Separate cold and warm runs and check runtime memory pressure.",
            "inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model --runs 3",
            "This command only uses user-supplied variance; it does not inspect runtime internals.",
        )
    if latency is not None and latency > 8.0:
        add(
            40,
            "Total latency is high for an interactive flow.",
            "Users may abandon the interaction before the answer completes.",
            "Shorten responses, reduce prompt/context size, and use a smaller or quantized model for demos.",
            "inferdoctor model fit --size {0} --quant {1} --vram {2}".format(model_size or "14b", quant or "q4", _fmt(vram_gib) if vram_gib is not None else "24"),
            "Total latency alone does not show which runtime stage is slow.",
        )
    if tps is not None and tps < 20:
        add(
            50,
            "Output speed is below 20 tokens/sec.",
            "Long answers will feel slow even with streaming.",
            "Prefer shorter answer style or a smaller model for chat-heavy workflows.",
            "inferdoctor optimize endpoint --streaming --tps {0:g}".format(tps),
            "TPS may be estimated unless the endpoint reports exact usage tokens.",
        )
    if context_tokens is not None and context_tokens > 8192:
        add(
            55,
            "Context size is large.",
            "Long prompts can delay TTFT and increase memory pressure.",
            "Reduce context budget, summarize retrieved context, or lower RAG top_k.",
            "inferdoctor optimize rag --top-k 4 --streaming",
            "Tokenization differs by model; this value is treated as a user-provided hint.",
        )
    if cpu_fallback_suspected:
        add(
            60,
            "CPU fallback is suspected.",
            "The runtime may be reachable but too slow for interactive use.",
            "Check GPU visibility, runtime logs, and model placement.",
            "inferdoctor check nvidia && inferdoctor check cuda",
            "InferDoctor cannot prove fallback from this advice-only command.",
        )
    if size_b and vram_gib:
        if size_b >= 32 and vram_gib <= 24:
            add(
                65,
                "A 32B-class model may be tight on 24 GiB or less VRAM.",
                "Memory pressure can increase TTFT or force fallback/offload.",
                "Use a 7B/8B or 14B quantized model for interactive demos before tuning larger models.",
                "inferdoctor model fit --size 32b --quant {0} --vram {1:g}".format(quant or "q4", vram_gib),
                "Actual fit depends on runtime overhead, context length, KV cache, and quantization format.",
            )
        elif size_b >= 14 and vram_gib < 16:
            add(
                66,
                "A 14B-class model may be oversized for this VRAM budget.",
                "Interactive TTFT and stability may suffer.",
                "Use q4 quantization or a smaller model size class.",
                "inferdoctor model fit --size {0} --quant {1} --vram {2:g}".format(model_size or "14b", quant or "q4", vram_gib),
                "This is a heuristic, not a memory profiler.",
            )
    if containerized or docker:
        add(
            70,
            "Docker or container networking is involved.",
            "localhost may refer to the container rather than the host endpoint.",
            "Verify host/container networking and daemon health before tuning the model.",
            "inferdoctor check docker",
            "InferDoctor does not start containers or inspect private compose files from this command.",
        )
    if runtime_label == "ollama":
        add(
            80,
            "Ollama is selected as the runtime.",
            "It is usually the easiest setup path, but model size and cold starts still matter.",
            "Use streaming clients, verify the local endpoint, and warm up the model before demos.",
            "inferdoctor check ollama",
            "InferDoctor does not install Ollama or pull models.",
        )
    elif runtime_label == "vllm":
        add(
            80,
            "vLLM is selected as the runtime.",
            "It can improve serving throughput, but batching and max model length can trade off with interactive TTFT.",
            "Verify the base URL ends with /v1 and tune max model length for your workload.",
            "inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1",
            "InferDoctor does not inspect vLLM scheduler, KV cache, or GPU utilization from this command.",
        )
    elif runtime_label == "sglang":
        add(
            80,
            "SGLang is selected as the runtime.",
            "Endpoint routing and runtime/model fit should be validated before optimizing app code.",
            "Check /v1 routing and streaming support with a tiny smoke test.",
            "inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1",
            "InferDoctor does not import or configure SGLang.",
        )
    elif runtime_label == "openai-compatible":
        add(
            90,
            "A generic OpenAI-compatible endpoint is selected.",
            "Runtime-specific assumptions may be wrong.",
            "Measure endpoint and streaming behavior first, then tune based on observed metrics.",
            "inferdoctor perf endpoint --endpoint http://127.0.0.1:8000/v1 --model local-model",
            "InferDoctor cannot infer runtime internals from a generic endpoint alone.",
        )

    if not bottlenecks:
        bottlenecks.append("No obvious bottleneck from the supplied facts; collect TTFT, total latency, and streaming behavior first.")
    quick_wins = [item for _, item in sorted(recommendations, key=lambda pair: pair[0])[:5]]
    if not quick_wins:
        quick_wins.append(
            "Observation: No concrete performance fact was supplied.\n"
            "Impact: Advice would be generic.\n"
            "Action: Run a bounded smoke test first.\n"
            "Next: inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model\n"
            "Limitation: Smoke tests are not formal benchmarks."
        )

    next_commands = [
        "inferdoctor perf endpoint --endpoint http://127.0.0.1:8000/v1 --model local-model",
        "inferdoctor perf streaming --endpoint http://127.0.0.1:8000/v1 --model local-model",
        "inferdoctor model fit --size {0} --quant {1} --vram {2}".format(model_size or "14b", quant or "q4", _fmt(vram_gib) if vram_gib is not None else "24"),
    ]
    caveats = [
        "This advice is heuristic and based only on supplied metrics; it is not a benchmark.",
        "Each recommendation is based only on supplied facts; omitted facts are not assumed.",
        "InferDoctor cannot see model architecture, KV cache settings, context length, batching, Docker networking, or GPU utilization from this command alone.",
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
    for index, item in enumerate(report.quick_wins, start=1):
        parts = item.splitlines()
        if not parts:
            continue
        lines.append("{0}. {1}".format(index, parts[0]))
        lines.extend("   {0}".format(part) for part in parts[1:])
    lines.extend(["", "Safe next commands:"])
    lines.extend("- {0}".format(item) for item in report.next_commands)
    lines.extend(["", "What InferDoctor cannot know yet:"])
    lines.extend("- {0}".format(item) for item in report.caveats)
    return "\n".join(lines)
