from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from inferdoctor.core.capacity import detect_hardware, estimate_model_memory_gib, parse_model_size_b


@dataclass(frozen=True)
class ModelFitResult:
    size_b: float
    quant: str
    runtime: Optional[str]
    vram_gib: Optional[float]
    estimated_memory_gib: float
    fit: str
    caveat: str


def estimate_model_fit(
    size: object,
    quant: str = "q4",
    runtime: Optional[str] = None,
    vram_gib: Optional[float] = None,
) -> ModelFitResult:
    size_b = parse_model_size_b(size)
    if size_b is None:
        size_b = 7.0
    resolved_vram = vram_gib
    if resolved_vram is None:
        resolved_vram = detect_hardware().vram_gib
    estimated = estimate_model_memory_gib(size_b, quant, runtime)
    if resolved_vram is None:
        fit = "MAYBE"
        caveat = "No VRAM figure was available; use --vram for a clearer estimate."
    elif resolved_vram >= estimated + 4:
        fit = "LIKELY FITS"
        caveat = "There appears to be memory headroom, but context length and runtime settings still matter."
    elif resolved_vram >= estimated:
        fit = "MAYBE"
        caveat = "Memory is close to the estimate; reduce context length or use a smaller quantization/runtime setting."
    else:
        fit = "UNLIKELY"
        caveat = "Estimated memory exceeds available VRAM; choose a smaller model, lower context, or CPU/offload fallback."
    return ModelFitResult(
        size_b=size_b,
        quant=quant,
        runtime=runtime,
        vram_gib=resolved_vram,
        estimated_memory_gib=estimated,
        fit=fit,
        caveat=caveat,
    )


def render_model_fit(result: ModelFitResult) -> str:
    vram = "unknown" if result.vram_gib is None else "{0:g} GiB".format(result.vram_gib)
    runtime = result.runtime or "generic"
    lines = [
        "InferDoctor Model Fit Advisor",
        "=" * 57,
        "Heuristic estimate only. This is not a benchmark.",
        "",
        "Request:",
        "  Model size: {0:g}B".format(result.size_b),
        "  Quantization: {0}".format(result.quant.upper()),
        "  Runtime: {0}".format(runtime),
        "  VRAM: {0}".format(vram),
        "",
        "Estimate:",
        "  Estimated memory: {0:.1f} GiB".format(result.estimated_memory_gib),
        "  Fit: {0}".format(result.fit),
        "  Caveat: {0}".format(result.caveat),
        "",
        "Next:",
        "  inferdoctor capacity --model-size {0:g}b --quant {1}{2}".format(
            result.size_b,
            result.quant,
            " --runtime " + result.runtime if result.runtime else "",
        ),
    ]
    return "\n".join(lines)
