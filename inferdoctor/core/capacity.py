from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import List, Optional

from inferdoctor.checkers.nvidia import NvidiaChecker
from inferdoctor.core.config import Config
from inferdoctor.core.models import Status


@dataclass(frozen=True)
class CapacityHardware:
    architecture: str
    total_ram_gib: Optional[float]
    available_ram_gib: Optional[float]
    vram_gib: Optional[float]
    gpu_name: Optional[str] = None
    vram_source: str = "detected"


@dataclass(frozen=True)
class CapacityRow:
    workload: str
    readiness: str
    note: str


def _meminfo_value(field: str) -> Optional[float]:
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as meminfo:
            for line in meminfo:
                if line.startswith(field + ":"):
                    return int(line.split()[1]) * 1024 / (1024 ** 3)
    except (OSError, ValueError, IndexError):
        return None
    return None


def _detect_vram() -> tuple[Optional[float], Optional[str]]:
    result = NvidiaChecker().run(Config())
    if result.status != Status.PASS:
        return None, None
    gpus = result.raw_data.get("gpus") or []
    best_memory = None
    best_name = None
    for gpu in gpus:
        memory_mib = gpu.get("memory_total_mib")
        if memory_mib is None:
            continue
        if best_memory is None or memory_mib > best_memory:
            best_memory = memory_mib
            best_name = str(gpu.get("name") or "NVIDIA GPU")
    if best_memory is None:
        return None, best_name
    return best_memory / 1024, best_name


def detect_hardware(
    vram_gib: Optional[float] = None,
    gpu_name: Optional[str] = None,
) -> CapacityHardware:
    detected_vram = vram_gib
    detected_gpu = gpu_name
    source = "override" if vram_gib is not None else "detected"
    if detected_vram is None:
        detected_vram, detected_gpu = _detect_vram()
    elif detected_gpu is None:
        detected_gpu = "manual VRAM override"
    return CapacityHardware(
        architecture=platform.machine() or "unknown",
        total_ram_gib=_meminfo_value("MemTotal"),
        available_ram_gib=_meminfo_value("MemAvailable"),
        vram_gib=detected_vram,
        gpu_name=detected_gpu,
        vram_source=source,
    )


def _at_least(value: Optional[float], threshold: float) -> bool:
    return value is not None and value >= threshold


def _either(
    vram: Optional[float],
    ram: Optional[float],
    vram_min: float,
    ram_min: float,
) -> bool:
    return _at_least(vram, vram_min) or _at_least(ram, ram_min)


def estimate_capacity(hardware: CapacityHardware) -> List[CapacityRow]:
    ram = hardware.total_ram_gib
    vram = hardware.vram_gib
    rows = [
        CapacityRow(
            "CPU-only local AI",
            "LIMITED" if not _at_least(ram, 16) else "POSSIBLE",
            (
                "Useful for embeddings, small models, and diagnostics; "
                "expect slower generation without GPU."
            ),
        )
    ]

    small_ok = _either(vram, ram, 6, 12)
    rows.append(
        CapacityRow(
            "Small local chat models",
            "LIKELY OK" if small_ok else "MAYBE",
            "Best with quantized models and conservative context length.",
        )
    )

    if _either(vram, ram, 8, 16):
        seven_b = "LIKELY OK"
    elif _either(vram, ram, 6, 12):
        seven_b = "MAYBE"
    else:
        seven_b = "UNLIKELY"
    rows.append(
        CapacityRow(
            "7B/8B quantized models",
            seven_b,
            "Heuristic assumes Q4-style quantization.",
        )
    )

    if _either(vram, ram, 16, 32):
        fourteen_b = "LIKELY OK"
    elif _either(vram, ram, 10, 20):
        fourteen_b = "MAYBE"
    else:
        fourteen_b = "UNLIKELY"
    rows.append(
        CapacityRow(
            "14B quantized models",
            fourteen_b,
            "May need lower context length or CPU offload.",
        )
    )

    if _either(vram, ram, 32, 64):
        thirty_two_b = "LIKELY OK"
    elif _either(vram, ram, 24, 48):
        thirty_two_b = "MAYBE"
    else:
        thirty_two_b = "UNLIKELY"
    rows.append(
        CapacityRow(
            "32B quantized models",
            thirty_two_b,
            "Memory headroom matters more than model name.",
        )
    )

    if _at_least(vram, 24):
        vllm = "LIKELY OK"
        vllm_note = (
            "Suitable for smaller FP16/BF16 serving; model and context still decide."
        )
    elif _at_least(vram, 16):
        vllm = "MEMORY LIMITED"
        vllm_note = "May work for smaller models with tight memory settings."
    else:
        vllm = "UNLIKELY"
        vllm_note = "vLLM FP16 serving usually needs substantial GPU memory."
    rows.append(CapacityRow("vLLM FP16 serving", vllm, vllm_note))

    if _either(vram, ram, 8, 16):
        ollama = "LIKELY OK"
    elif _either(vram, ram, 4, 8):
        ollama = "MAYBE"
    else:
        ollama = "UNLIKELY"
    rows.append(
        CapacityRow(
            "Ollama quantized usage",
            ollama,
            "Ollama-style quantized models are the intended fit for this estimate.",
        )
    )
    return rows


def _fmt_gib(value: Optional[float]) -> str:
    if value is None:
        return "unknown"
    return "{0:.1f} GiB".format(value)


def render_capacity(
    vram_gib: Optional[float] = None,
    gpu_name: Optional[str] = None,
) -> str:
    hardware = detect_hardware(vram_gib=vram_gib, gpu_name=gpu_name)
    rows = estimate_capacity(hardware)
    gpu_label = hardware.gpu_name or "none detected"
    vram_label = _fmt_gib(hardware.vram_gib)
    if hardware.vram_source == "override":
        vram_label += " (override)"
    lines = [
        "InferDoctor Capacity Preview",
        "=" * 57,
        "Heuristic estimate only. No models are downloaded or run.",
        "",
        "Detected hardware:",
        "  CPU architecture: {0}".format(hardware.architecture),
        "  System RAM: {0} total, {1} available".format(
            _fmt_gib(hardware.total_ram_gib), _fmt_gib(hardware.available_ram_gib)
        ),
        "  NVIDIA VRAM: {0}".format(vram_label),
        "  GPU: {0}".format(gpu_label),
        "",
        "Workload readiness:",
        "Workload                    Readiness       Notes",
        "--------------------------  --------------  ----------------------------------------",
    ]
    for row in rows:
        lines.append(
            "{0:<26}  {1:<14}  {2}".format(
                row.workload[:26], row.readiness, row.note
            )
        )
    lines.extend([
        "",
        "Capacity estimates are rough heuristics, not benchmarks.",
        "Use inferdoctor check for actual stack health diagnostics.",
    ])
    return "\n".join(lines)
