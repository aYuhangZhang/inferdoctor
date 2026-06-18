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


@dataclass(frozen=True)
class StackBootstrapPlan:
    recommendation: StackRecommendation
    project_path: str
    commands: List[str]
    safe_actions: List[str]
    requires_approval: List[str]
    will_not_do: List[str]


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
        "inferdoctor template smoke-test {0}".format(template_dir),
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
        "Use-case fit:",
    ]
    lines.extend("  - {0}".format(item) for item in rec.use_case_guidance)
    lines.extend([
        "",
        "Required components:",
    ])
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


def build_stack_bootstrap_plan(
    goal: Optional[str] = None,
    preference: Optional[str] = None,
    hardware: str = "auto",
    vram_gib: Optional[float] = None,
    output_dir: Optional[str] = None,
) -> StackBootstrapPlan:
    recommendation = recommend_stack(
        goal=goal,
        preference=preference,
        hardware=hardware,
        vram_gib=vram_gib,
    )
    project_path = output_dir or "./{0}-demo".format(recommendation.template)
    commands = [
        "inferdoctor",
        "inferdoctor recommend --goal {0}".format(recommendation.goal),
        "inferdoctor template create {0} --output {1}".format(recommendation.template, project_path),
        "inferdoctor template validate {0}".format(project_path),
        "inferdoctor template smoke-test {0}".format(project_path),
        "cd {0}".format(project_path),
        "cp .env.example .env",
        "python app.py --dry-run" if recommendation.template in {"customer-service", "restaurant-ordering"} else "python query.py --dry-run",
        "python app.py --check-config" if recommendation.template in {"customer-service", "restaurant-ordering"} else "python query.py --check-config",
    ]
    safe_actions = [
        "Show this plan without changing files.",
        "Generate a starter project only when the user runs the template create command.",
        "Validate files and run dry-run smoke commands without contacting endpoints.",
    ]
    requires_approval = [
        "Installing any local AI runtime or Python dependency.",
        "Starting Docker containers or background services.",
        "Calling a live model endpoint with user data.",
    ]
    will_not_do = [
        "Install Ollama, vLLM, SGLang, Xinference, CUDA, or GPU frameworks.",
        "Download models.",
        "Run model inference.",
        "Modify system settings or start services.",
    ]
    return StackBootstrapPlan(
        recommendation=recommendation,
        project_path=project_path,
        commands=commands,
        safe_actions=safe_actions,
        requires_approval=requires_approval,
        will_not_do=will_not_do,
    )


def render_stack_bootstrap_plan(plan: StackBootstrapPlan) -> str:
    rec = plan.recommendation
    lines = [
        "InferDoctor Stack Bootstrap Plan (Dry Run)",
        "=" * 57,
        "Goal: {0}".format(rec.goal),
        "Preference: {0}".format(rec.preference),
        "Recommended runtime: {0}".format(rec.runtime),
        "Recommended template: {0}".format(rec.template),
        "Generated project path: {0}".format(plan.project_path),
        "Model size class: {0}".format(rec.model_size_class),
        "",
        "Commands that would be run by a careful beginner:",
    ]
    lines.extend("  {0}. {1}".format(index, command) for index, command in enumerate(plan.commands, start=1))
    lines.extend(["", "What is safe in this dry run:"])
    lines.extend("  - {0}".format(item) for item in plan.safe_actions)
    lines.extend(["", "Requires explicit user approval:"])
    lines.extend("  - {0}".format(item) for item in plan.requires_approval)
    lines.extend(["", "InferDoctor will not do automatically:"])
    lines.extend("  - {0}".format(item) for item in plan.will_not_do)
    lines.extend([
        "",
        "Next command to actually create files:",
        "  inferdoctor template create {0} --output {1}".format(rec.template, plan.project_path),
    ])
    return "\n".join(lines)
