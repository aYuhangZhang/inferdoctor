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
    why: str
    caveats: str


def _model_size_for(vram_gib: Optional[float], preference: str) -> str:
    if vram_gib is None:
        return "Small quantized model first; use inferdoctor capacity for a better estimate"
    if vram_gib >= 48:
        return "14B or 32B quantized; larger serving depends on runtime settings"
    if vram_gib >= 24:
        return "7B or 14B quantized"
    if vram_gib >= 12:
        return "7B/8B quantized"
    if preference == "cpu":
        return "small CPU-friendly quantized model"
    return "small quantized model with conservative context"


def _runtime_for(goal: str, preference: str, vram_gib: Optional[float]) -> str:
    if preference == "easiest" or preference == "cpu":
        return "Ollama"
    if goal == "document-qa" and preference == "easiest":
        return "Ollama plus a simple document template"
    if goal == "local-api":
        if vram_gib is not None and vram_gib >= 16:
            return "vLLM or SGLang"
        return "LM Studio or llama.cpp server first; vLLM/SGLang after GPU headroom is confirmed"
    if vram_gib is not None and vram_gib >= 24:
        return "Ollama for easiest setup, vLLM for higher throughput"
    if vram_gib is not None and vram_gib >= 12:
        return "Ollama first; consider vLLM only with careful memory settings"
    return "Ollama or llama.cpp-style CPU fallback"


def recommend_stack(
    goal: Optional[str] = None,
    preference: Optional[str] = None,
    hardware: str = "auto",
    vram_gib: Optional[float] = None,
) -> StackRecommendation:
    setup = recommend_setup(goal, preference)
    resolved_vram = vram_gib
    hardware_label = hardware
    if resolved_vram is None and hardware == "auto":
        detected = detect_hardware()
        resolved_vram = detected.vram_gib
        hardware_label = detected.gpu_name or detected.architecture or "auto"
    runtime = _runtime_for(setup.goal, setup.preference, resolved_vram)
    model_size = _model_size_for(resolved_vram, setup.preference)
    why = (
        "The recommendation balances your goal, preference, and available VRAM."
        if resolved_vram is not None
        else "No reliable VRAM figure was provided, so the recommendation starts conservatively."
    )
    caveats = "Heuristic only: verify the endpoint with inferdoctor check before building on it."
    return StackRecommendation(
        goal=setup.goal,
        preference=setup.preference,
        hardware=hardware_label,
        vram_gib=resolved_vram,
        runtime=runtime,
        model_size_class=model_size,
        template=setup.template,
        why=why,
        caveats=caveats,
    )


def render_recommendation(recommendation: StackRecommendation) -> str:
    vram = "unknown" if recommendation.vram_gib is None else "{0:g} GiB".format(recommendation.vram_gib)
    lines = [
        "InferDoctor Stack Recommendation",
        "=" * 57,
        "Goal: {0}".format(recommendation.goal),
        "Preference: {0}".format(recommendation.preference),
        "Hardware: {0}".format(recommendation.hardware),
        "VRAM: {0}".format(vram),
        "",
        "Recommendation:",
        "  Runtime: {0}".format(recommendation.runtime),
        "  Model size: {0}".format(recommendation.model_size_class),
        "  Template: {0}".format(recommendation.template),
        "  Why: {0}".format(recommendation.why),
        "",
        "Next commands:",
        "  inferdoctor check",
        "  inferdoctor capacity --vram {0}".format(recommendation.vram_gib) if recommendation.vram_gib is not None else "  inferdoctor capacity",
        "  inferdoctor template create {0} --output ./{0}-demo".format(recommendation.template),
        "",
        "Caveats:",
        "  {0}".format(recommendation.caveats),
    ]
    return "\n".join(lines)
