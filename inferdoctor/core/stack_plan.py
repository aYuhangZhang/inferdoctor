from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from inferdoctor.core.recommendations import StackRecommendation, recommend_stack


@dataclass(frozen=True)
class LocalAIStackPlan:
    recommendation: StackRecommendation
    required_components: List[str]
    optional_components: List[str]
    steps: List[str]
    commands: List[str]
    warnings: List[str]


def _required_components(goal: str, runtime: str) -> list[str]:
    components = ["Python 3.9+", "A local OpenAI-compatible model endpoint"]
    lowered = runtime.lower()
    if "ollama" in lowered:
        components.append("Ollama or another simple local runtime")
    if "vllm" in lowered or "sglang" in lowered:
        components.append("NVIDIA GPU with enough VRAM for the selected model")
    if goal == "document-qa":
        components.append("Local Markdown documents")
    return components


def _optional_components(goal: str, runtime: str) -> list[str]:
    components = ["Open WebUI for browser chat", "Docker if your preferred runtime uses containers"]
    if goal == "document-qa":
        components.extend(["Dify for a fuller RAG app", "Embedding service when you outgrow keyword retrieval"])
    if "vllm" not in runtime.lower():
        components.append("vLLM later for higher throughput")
    if "sglang" not in runtime.lower():
        components.append("SGLang later for OpenAI-compatible serving experiments")
    return components


def build_stack_plan(
    goal: Optional[str] = None,
    preference: Optional[str] = None,
    hardware: str = "auto",
    vram_gib: Optional[float] = None,
) -> LocalAIStackPlan:
    recommendation = recommend_stack(
        goal=goal,
        preference=preference,
        hardware=hardware,
        vram_gib=vram_gib,
    )
    template_dir = "./{0}-demo".format(recommendation.template)
    steps = [
        "Run the health check first so endpoint and GPU problems are visible early.",
        "Create the starter project for your goal.",
        "Validate the generated files before editing them.",
        "Configure LOCAL_AI_BASE_URL and LOCAL_AI_MODEL in .env or config.yaml.",
        "Run the generated app and keep InferDoctor nearby for endpoint troubleshooting.",
    ]
    commands = [
        "inferdoctor",
        "inferdoctor recommend --goal {0}".format(recommendation.goal),
        "inferdoctor template create {0} --output {1}".format(recommendation.template, template_dir),
        "inferdoctor template validate {0}".format(template_dir),
        "inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1",
        "inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1",
    ]
    warnings = [
        "This is a heuristic setup plan, not a benchmark or hardware guarantee.",
        "InferDoctor does not install runtimes, download models, run inference, or modify system settings by default.",
    ]
    if recommendation.vram_gib is None:
        warnings.append("VRAM was not detected or provided; add --vram for a clearer model-size recommendation.")
    return LocalAIStackPlan(
        recommendation=recommendation,
        required_components=_required_components(recommendation.goal, recommendation.runtime),
        optional_components=_optional_components(recommendation.goal, recommendation.runtime),
        steps=steps,
        commands=commands,
        warnings=warnings,
    )


def render_stack_plan(plan: LocalAIStackPlan) -> str:
    rec = plan.recommendation
    vram = "unknown" if rec.vram_gib is None else "{0:g} GiB".format(rec.vram_gib)
    lines = [
        "InferDoctor Local AI Stack Plan",
        "=" * 57,
        "Goal: {0}".format(rec.goal),
        "Preference: {0}".format(rec.preference),
        "Hardware: {0}".format(rec.hardware),
        "VRAM: {0}".format(vram),
        "",
        "Recommended path:",
        "  Runtime: {0}".format(rec.runtime),
        "  Model size class: {0}".format(rec.model_size_class),
        "  Starter template: {0}".format(rec.template),
        "  Why: {0}".format(rec.why),
        "",
        "Required components:",
    ]
    lines.extend("  - {0}".format(component) for component in plan.required_components)
    lines.extend(["", "Optional components:"])
    lines.extend("  - {0}".format(component) for component in plan.optional_components)
    lines.extend(["", "Step-by-step next actions:"])
    lines.extend("  {0}. {1}".format(index, step) for index, step in enumerate(plan.steps, start=1))
    lines.extend(["", "Commands to run:"])
    lines.extend("  {0}".format(command) for command in plan.commands)
    lines.extend(["", "Warnings and caveats:"])
    lines.extend("  - {0}".format(warning) for warning in plan.warnings)
    return "\n".join(lines)
