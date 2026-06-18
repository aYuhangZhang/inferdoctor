from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from inferdoctor.core.capacity import detect_hardware
from inferdoctor.core.setup import GOALS, PREFERENCES, recommend_setup


@dataclass(frozen=True)
class StackRecommendation:
    goal: str
    preference: str
    hardware: str
    vram_gib: Optional[float]
    runtime: str
    model_size_class: str
    template: str
    fit_label: str
    why: str
    easiest_path: str
    performance_path: str
    caveats: str
    unknowns: str


def _model_size_for(vram_gib: Optional[float], preference: str) -> str:
    if vram_gib is None:
        return "Small quantized model first; use inferdoctor capacity for a better estimate"
    if vram_gib >= 48:
        return "14B or 32B quantized; larger FP16 serving depends on runtime settings"
    if vram_gib >= 24:
        return "7B or 14B quantized"
    if vram_gib >= 12:
        return "7B/8B quantized"
    if preference == "cpu":
        return "small CPU-friendly quantized model"
    return "small quantized model with conservative context"


def _fit_label(vram_gib: Optional[float], preference: str) -> str:
    if vram_gib is None:
        return "MAYBE - hardware memory was not detected or provided"
    if vram_gib >= 24:
        return "LIKELY OK for a practical local demo"
    if vram_gib >= 8:
        return "MAYBE - use smaller quantized models and conservative context"
    if preference == "cpu":
        return "LIKELY OK for CPU-only experiments, but slower"
    return "LIMITED - start with the smallest local model path"


def _runtime_for(goal: str, preference: str, vram_gib: Optional[float]) -> str:
    if preference == "easiest" or preference == "cpu":
        return "Ollama"
    if goal == "local-api":
        if vram_gib is not None and vram_gib >= 16:
            return "vLLM or SGLang"
        return "LM Studio or llama.cpp server first; vLLM/SGLang after GPU headroom is confirmed"
    if vram_gib is not None and vram_gib >= 24:
        return "Ollama for easiest setup, vLLM for higher throughput"
    if vram_gib is not None and vram_gib >= 12:
        return "Ollama first; consider vLLM only with careful memory settings"
    return "Ollama or llama.cpp-style CPU fallback"


def _paths_for(goal: str, template: str, vram_gib: Optional[float]) -> tuple[str, str]:
    if template in {"customer-service", "restaurant-ordering", "local-doc-qa"}:
        easiest = "Use Ollama or LM Studio with an OpenAI-compatible endpoint, then create the {0} template.".format(template)
    else:
        easiest = "Use Ollama or LM Studio first, then inspect the {0} template guidance.".format(template)
    if vram_gib is not None and vram_gib >= 16:
        performance = "Use vLLM or SGLang after confirming the endpoint with inferdoctor check."
    else:
        performance = "Postpone vLLM/SGLang until GPU VRAM and driver readiness are confirmed."
    return easiest, performance


def recommend_stack(
    goal: Optional[str] = None,
    preference: Optional[str] = None,
    hardware: str = "auto",
    vram_gib: Optional[float] = None,
) -> StackRecommendation:
    setup = recommend_setup(goal, preference)
    resolved_vram = vram_gib
    hardware_label = "provided VRAM override" if vram_gib is not None and hardware == "auto" else hardware
    if resolved_vram is None and hardware == "auto":
        detected = detect_hardware()
        resolved_vram = detected.vram_gib
        hardware_label = detected.gpu_name or detected.architecture or "auto"
    runtime = _runtime_for(setup.goal, setup.preference, resolved_vram)
    model_size = _model_size_for(resolved_vram, setup.preference)
    easiest_path, performance_path = _paths_for(setup.goal, setup.template, resolved_vram)
    why = (
        "The recommendation balances your goal, preference, and available VRAM."
        if resolved_vram is not None
        else "No reliable VRAM figure was provided, so the recommendation starts conservatively."
    )
    caveats = "Model size, context length, quantization, concurrent users, and runtime flags can change memory use."
    unknowns = "InferDoctor does not know which exact model, context length, prompt load, or server flags you will use yet."
    return StackRecommendation(
        goal=setup.goal,
        preference=setup.preference,
        hardware=hardware_label,
        vram_gib=resolved_vram,
        runtime=runtime,
        model_size_class=model_size,
        template=setup.template,
        fit_label=_fit_label(resolved_vram, setup.preference),
        why=why,
        easiest_path=easiest_path,
        performance_path=performance_path,
        caveats=caveats,
        unknowns=unknowns,
    )


def _fmt_number(value: float) -> str:
    return "{0:g}".format(value)


def render_recommendation(recommendation: StackRecommendation) -> str:
    vram = "unknown" if recommendation.vram_gib is None else "{0:g} GiB".format(recommendation.vram_gib)
    lines = [
        "InferDoctor Stack Recommendation",
        "=" * 57,
        "Goal: {0}".format(recommendation.goal),
        "Preference: {0}".format(recommendation.preference),
        "Hardware: {0}".format(recommendation.hardware),
        "VRAM: {0}".format(vram),
        "Practical fit: {0}".format(recommendation.fit_label),
        "",
        "Recommendation:",
        "  Runtime: {0}".format(recommendation.runtime),
        "  Model size class: {0}".format(recommendation.model_size_class),
        "  Template: {0}".format(recommendation.template),
        "  Why: {0}".format(recommendation.why),
        "",
        "Runtime paths:",
        "  Easiest: {0}".format(recommendation.easiest_path),
        "  Performance: {0}".format(recommendation.performance_path),
        "",
        "Next commands:",
        "  inferdoctor",
        "  inferdoctor capacity --vram {0}".format(_fmt_number(recommendation.vram_gib)) if recommendation.vram_gib is not None else "  inferdoctor capacity",
        (
            "  inferdoctor template create {0} --output ./{0}-demo".format(recommendation.template)
            if recommendation.template in {"customer-service", "restaurant-ordering", "local-doc-qa"}
            else "  inferdoctor template show {0}".format(recommendation.template)
        ),
        (
            "  inferdoctor template validate ./{0}-demo".format(recommendation.template)
            if recommendation.template in {"customer-service", "restaurant-ordering", "local-doc-qa"}
            else "  inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1"
        ),
        "",
        "Memory caveats:",
        "  {0}".format(recommendation.caveats),
        "",
        "What InferDoctor does not know yet:",
        "  {0}".format(recommendation.unknowns),
    ]
    return "\n".join(lines)
