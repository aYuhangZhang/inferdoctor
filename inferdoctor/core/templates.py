from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class TemplateInfo:
    name: str
    title: str
    description: str
    target_user: str
    required_stack: List[str]
    optional_stack: List[str]
    hardware_recommendation: str
    estimated_difficulty: str
    generated_files_planned: List[str]
    next_command: str


TEMPLATES: Dict[str, TemplateInfo] = {
    "customer-service": TemplateInfo(
        name="customer-service",
        title="Customer Service Chatbot",
        description="A local FAQ assistant for small support teams or product sites.",
        target_user="Teams that want a simple local support chatbot before adding RAG.",
        required_stack=["OpenAI-compatible local endpoint"],
        optional_stack=["Ollama", "vLLM", "SGLang", "Dify"],
        hardware_recommendation="CPU works for small tests; NVIDIA GPU improves latency.",
        estimated_difficulty="easy",
        generated_files_planned=["README.md", "app.py", "requirements.txt", ".env.example", "data/faq.md", "config.yaml"],
        next_command="inferdoctor template create customer-service --output ./customer-service-demo",
    ),
    "restaurant-ordering": TemplateInfo(
        name="restaurant-ordering",
        title="Restaurant Ordering Assistant",
        description="A local ordering helper with menu data and clear ordering policies.",
        target_user="Restaurants or demo builders who need a concrete local chatbot scenario.",
        required_stack=["OpenAI-compatible local endpoint"],
        optional_stack=["Ollama", "LM Studio", "Open WebUI"],
        hardware_recommendation="Runs as a small demo on CPU; GPU helps interactive response time.",
        estimated_difficulty="easy",
        generated_files_planned=["README.md", "app.py", "requirements.txt", ".env.example", "data/menu.yaml", "data/policies.md", "config.yaml"],
        next_command="inferdoctor template create restaurant-ordering --output ./restaurant-ordering-demo",
    ),
    "local-doc-qa": TemplateInfo(
        name="local-doc-qa",
        title="Local Document Q&A",
        description="A starter for asking questions over local Markdown documents.",
        target_user="Developers building a small document assistant before adding a vector DB.",
        required_stack=["OpenAI-compatible local endpoint"],
        optional_stack=["Dify", "Xinference", "embedding endpoint"],
        hardware_recommendation="CPU is fine for keyword fallback; GPU helps generation.",
        estimated_difficulty="medium",
        generated_files_planned=["README.md", "ingest.py", "query.py", "requirements.txt", "docs/sample.md", "config.yaml"],
        next_command="inferdoctor template create local-doc-qa --output ./local-doc-qa-demo",
    ),
    "personal-kb": TemplateInfo(
        name="personal-kb",
        title="Personal Knowledge Base",
        description="A personal notes assistant that can later grow into local RAG.",
        target_user="Individual developers organizing private notes locally.",
        required_stack=["OpenAI-compatible local endpoint"],
        optional_stack=["Dify", "Open WebUI", "embedding endpoint"],
        hardware_recommendation="CPU is enough for early notes experiments.",
        estimated_difficulty="medium",
        generated_files_planned=["README.md", "config.yaml", "notes/sample.md"],
        next_command="inferdoctor template show local-doc-qa",
    ),
    "meeting-notes": TemplateInfo(
        name="meeting-notes",
        title="Meeting Notes Assistant",
        description="A local summarization workflow for pasted meeting notes.",
        target_user="Teams that want local-first meeting note cleanup.",
        required_stack=["OpenAI-compatible local endpoint"],
        optional_stack=["Ollama", "LM Studio"],
        hardware_recommendation="Small quantized models are usually enough.",
        estimated_difficulty="easy",
        generated_files_planned=["README.md", "summarize.py", "examples/meeting.txt"],
        next_command="inferdoctor template show meeting-notes",
    ),
    "openai-compatible-api": TemplateInfo(
        name="openai-compatible-api",
        title="OpenAI-compatible API Demo",
        description="A minimal client for any local /v1/chat/completions endpoint.",
        target_user="Developers validating local API compatibility.",
        required_stack=["OpenAI-compatible local endpoint"],
        optional_stack=["vLLM", "SGLang", "LM Studio", "llama.cpp server"],
        hardware_recommendation="Depends on the serving runtime and model size.",
        estimated_difficulty="easy",
        generated_files_planned=["README.md", "client.py", ".env.example"],
        next_command="inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1",
    ),
    "ollama-chat": TemplateInfo(
        name="ollama-chat",
        title="Ollama Chat Starter",
        description="A beginner-friendly local chat path using Ollama-style setup.",
        target_user="Beginners who want the easiest local chat workflow.",
        required_stack=["Ollama API or OpenAI-compatible endpoint"],
        optional_stack=["Open WebUI"],
        hardware_recommendation="CPU works for small models; GPU improves speed.",
        estimated_difficulty="easy",
        generated_files_planned=["README.md", "chat.py", "config.yaml"],
        next_command="inferdoctor check ollama",
    ),
    "dify-rag": TemplateInfo(
        name="dify-rag",
        title="Dify Local RAG Starter",
        description="A readiness path for running a Dify-backed local RAG app.",
        target_user="Developers using Dify as the app layer.",
        required_stack=["Dify endpoint", "model endpoint"],
        optional_stack=["Xinference", "Ollama", "vLLM"],
        hardware_recommendation="Match hardware to the selected model endpoint.",
        estimated_difficulty="medium",
        generated_files_planned=["README.md", "inferdoctor.yaml", "sample_prompt.md"],
        next_command="inferdoctor check dify --endpoint http://127.0.0.1:5001",
    ),
    "open-webui": TemplateInfo(
        name="open-webui",
        title="Open WebUI Starter",
        description="A setup path for diagnosing Open WebUI plus a local backend.",
        target_user="Users who prefer a browser UI for local chat.",
        required_stack=["Open WebUI", "model backend"],
        optional_stack=["Ollama", "OpenAI-compatible endpoint"],
        hardware_recommendation="Backend model decides the hardware need.",
        estimated_difficulty="easy",
        generated_files_planned=["README.md", "inferdoctor.yaml"],
        next_command="inferdoctor check openwebui",
    ),
    "vllm-api": TemplateInfo(
        name="vllm-api",
        title="vLLM API Starter",
        description="A high-throughput local API readiness path for vLLM.",
        target_user="Developers serving OpenAI-compatible APIs on NVIDIA GPUs.",
        required_stack=["NVIDIA GPU", "vLLM OpenAI-compatible endpoint"],
        optional_stack=["Docker", "CUDA toolkit for builds"],
        hardware_recommendation="Prefer 16 GiB+ VRAM; 24 GiB+ gives more headroom.",
        estimated_difficulty="advanced",
        generated_files_planned=["README.md", "client.py", "inferdoctor.yaml"],
        next_command="inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1",
    ),
    "sglang-api": TemplateInfo(
        name="sglang-api",
        title="SGLang API Starter",
        description="A local API readiness path for SGLang OpenAI-compatible serving.",
        target_user="Developers testing SGLang servers and API clients.",
        required_stack=["NVIDIA GPU", "SGLang OpenAI-compatible endpoint"],
        optional_stack=["Docker", "CUDA toolkit for builds"],
        hardware_recommendation="Prefer 16 GiB+ VRAM; tune model and context to fit.",
        estimated_difficulty="advanced",
        generated_files_planned=["README.md", "client.py", "inferdoctor.yaml"],
        next_command="inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1",
    ),
}


def list_templates() -> List[TemplateInfo]:
    return [TEMPLATES[name] for name in sorted(TEMPLATES)]


def get_template(name: str) -> TemplateInfo:
    try:
        return TEMPLATES[name]
    except KeyError as exc:
        available = ", ".join(sorted(TEMPLATES))
        raise KeyError("unknown template '{0}'. Available templates: {1}".format(name, available)) from exc


def template_names() -> List[str]:
    return sorted(TEMPLATES)


def _join(values: Iterable[str]) -> str:
    return ", ".join(values) if values else "none"


def render_template_list() -> str:
    lines = [
        "InferDoctor Local AI Templates",
        "=" * 57,
        "Starter ideas for turning a diagnosed machine into a local AI app.",
        "No files are generated by this command.",
        "",
        "Template                   Difficulty  Required stack",
        "-------------------------  ----------  ------------------------------",
    ]
    for template in list_templates():
        required = _join(template.required_stack)
        lines.append("{0:<25}  {1:<10}  {2}".format(template.name, template.estimated_difficulty, required[:30]))
    lines.extend([
        "",
        "Show details:",
        "  inferdoctor template show customer-service",
        "",
        "Create a starter project:",
        "  inferdoctor template create customer-service --output ./customer-service-demo",
    ])
    return "\n".join(lines)


def render_template_detail(name: str) -> str:
    template = get_template(name)
    lines = [
        "InferDoctor Template: {0}".format(template.name),
        "=" * 57,
        template.title,
        "",
        template.description,
        "",
        "Target user: {0}".format(template.target_user),
        "Required stack: {0}".format(_join(template.required_stack)),
        "Optional stack: {0}".format(_join(template.optional_stack)),
        "Hardware: {0}".format(template.hardware_recommendation),
        "Difficulty: {0}".format(template.estimated_difficulty),
        "",
        "Generated files planned:",
    ]
    lines.extend("  - {0}".format(item) for item in template.generated_files_planned)
    lines.extend([
        "",
        "Next command:",
        "  {0}".format(template.next_command),
    ])
    return "\n".join(lines)
