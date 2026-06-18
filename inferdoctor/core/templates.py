from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
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
        "InferDoctor Local AI App Templates",
        "=" * 57,
        "Pick a small starter app after your machine and endpoint look healthy.",
        "This command only shows options. It does not create files.",
        "",
    ]
    for template in list_templates():
        lines.extend([
            "{0}  ({1})".format(template.name, template.estimated_difficulty),
            "  Builds: {0}".format(template.title),
            "  Needs: {0}".format(_join(template.required_stack)),
            "  Good for: {0}".format(template.target_user),
            "",
        ])
    lines.extend([
        "Next steps:",
        "  1. Show details: inferdoctor template show customer-service",
        "  2. Create a starter: inferdoctor template create customer-service --output ./customer-service-demo",
        "  3. Configure the generated .env or config.yaml for your local endpoint.",
    ])
    return "\n".join(lines)


def render_template_detail(name: str) -> str:
    template = get_template(name)
    lines = [
        "InferDoctor Template: {0}".format(template.name),
        "=" * 57,
        template.title,
        "",
        "What it builds:",
        "  {0}".format(template.description),
        "",
        "Who it is for:",
        "  {0}".format(template.target_user),
        "",
        "Stack fit:",
        "  Required: {0}".format(_join(template.required_stack)),
        "  Optional: {0}".format(_join(template.optional_stack)),
        "  Hardware: {0}".format(template.hardware_recommendation),
        "  Difficulty: {0}".format(template.estimated_difficulty),
        "",
        "Files planned:",
    ]
    lines.extend("  - {0}".format(item) for item in template.generated_files_planned)
    lines.extend([
        "",
        "Beginner path:",
        "  1. Run inferdoctor to check the machine.",
        "  2. Create this starter project.",
        "  3. Edit .env or config.yaml to point at your local endpoint.",
        "  4. Run the generated app from its README.",
        "",
        "Create it:",
        "  {0}".format(template.next_command),
    ])
    return "\n".join(lines)



DEFAULT_ENDPOINT = "http://127.0.0.1:8000/v1"


def _base_readme(title: str, purpose: str, command: str) -> str:
    return """# {title}

{purpose}

This starter is generated by InferDoctor for a local OpenAI-compatible endpoint.
It does not require a cloud API key by default.

## Requirements

- Python 3.9+
- A local OpenAI-compatible endpoint, for example vLLM, SGLang, LM Studio, or llama.cpp server

## Configure

Edit `config.yaml` or set environment variables:

```bash
export LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1
export LOCAL_AI_MODEL=local-model
```

## Run

```bash
{command}
```

## Diagnose

```bash
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
```

## Example Prompts

Try prompts such as:

- What can you help me with?
- Summarize the available context.
- What should I check if the local endpoint fails?

## Troubleshooting

If the app cannot connect, run:

```bash
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor explain openai-compatible-connection-refused
```

If the response shape looks wrong, verify that your runtime exposes an OpenAI-compatible `/v1/chat/completions` route.

## Safety

The template sends prompts only to the endpoint you configure. Keep it pointed at a local service if you want a local-only demo.
""".format(title=title, purpose=purpose, command=command)


def _chat_client_py(system_prompt: str, data_loader: str) -> str:
    return """from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

BASE_URL = os.environ.get("LOCAL_AI_BASE_URL", "{endpoint}").rstrip("/")
MODEL = os.environ.get("LOCAL_AI_MODEL", "local-model")
SYSTEM_PROMPT = {system_prompt!r}


def load_context() -> str:
{data_loader}


def ask_local_model(message: str) -> str:
    payload = {{
        "model": MODEL,
        "messages": [
            {{"role": "system", "content": SYSTEM_PROMPT + "\\n\\nContext:\\n" + load_context()}},
            {{"role": "user", "content": message}},
        ],
        "temperature": 0.2,
    }}
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=data,
        headers={{"Content-Type": "application/json"}},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return "Could not reach local endpoint at {{0}}: {{1}}".format(BASE_URL, exc)
    except json.JSONDecodeError:
        return "Endpoint responded, but the response was not valid JSON."

    try:
        return body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return "Endpoint response did not look like OpenAI chat completions JSON."


def main() -> None:
    print("Local AI starter. Type 'exit' to quit.")
    while True:
        try:
            message = input("you> ").strip()
        except EOFError:
            break
        if message.lower() in {{"exit", "quit"}}:
            break
        if not message:
            continue
        print("assistant> " + ask_local_model(message))


if __name__ == "__main__":
    main()
""".format(endpoint=DEFAULT_ENDPOINT, system_prompt=system_prompt, data_loader=data_loader)


def _customer_service_files() -> dict[str, str]:
    data_loader = '    with open("data/faq.md", "r", encoding="utf-8") as faq:\n        return faq.read()'
    return {
        "README.md": _base_readme(
            "Customer Service Chatbot",
            "A local FAQ assistant for answering product and support questions.",
            "python app.py",
        ),
        "app.py": _chat_client_py(
            "You are a concise customer service assistant. Answer only from the FAQ context. If the answer is missing, say you do not know and suggest contacting support.",
            data_loader,
        ),
        "requirements.txt": "# Standard library only. Add packages here if you extend the demo.\n",
        ".env.example": "LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1\nLOCAL_AI_MODEL=local-model\n",
        "data/faq.md": """# Example FAQ

## Shipping
Standard shipping usually takes 3-5 business days. Expedited shipping takes 1-2 business days when available.

## Returns
Unused items can be returned within 30 days with the original receipt. Opened software, personalized items, and gift cards are not refundable.

## Warranty
Hardware accessories include a one-year limited warranty against manufacturing defects.

## Account Help
Customers can reset their password from the sign-in page. Support cannot view or share passwords.

## Support Hours
Support is available Monday to Friday, 09:00-18:00 local time. Urgent outage reports are monitored after hours.
""",
        "config.yaml": "endpoint: http://127.0.0.1:8000/v1\nmodel: local-model\n",
    }


def _restaurant_ordering_files() -> dict[str, str]:
    data_loader = '    parts = []\n    for filename in ("data/menu.yaml", "data/policies.md"):\n        with open(filename, "r", encoding="utf-8") as handle:\n            parts.append(handle.read())\n    return "\\n\\n".join(parts)'
    return {
        "README.md": _base_readme(
            "Restaurant Ordering Assistant",
            "A local restaurant ordering assistant with menu and policy context.",
            "python app.py",
        ),
        "app.py": _chat_client_py(
            "You are a restaurant ordering assistant. Help users choose items, clarify options, and follow the ordering policies. Do not invent unavailable menu items.",
            data_loader,
        ),
        "requirements.txt": "# Standard library only. Add packages here if you extend the demo.\n",
        ".env.example": "LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1\nLOCAL_AI_MODEL=local-model\n",
        "data/menu.yaml": """restaurant: Local Noodle House
currency: USD
items:
  - name: Classic Ramen
    price: 12
    options: [mild, spicy, extra spicy]
    allergens: [wheat, soy]
  - name: Miso Ramen
    price: 13
    options: [pork, chicken, tofu]
    allergens: [soy]
  - name: Vegetable Rice Bowl
    price: 10
    options: [regular, large]
    allergens: [sesame]
  - name: Gyoza
    price: 6
    options: [pork, vegetable]
  - name: Iced Tea
    price: 3
  - name: Sparkling Water
    price: 2
""",
        "data/policies.md": """# Ordering Policies

- Confirm pickup or dine-in before finalizing an order.
- Ask about spice level when ramen is selected.
- Ask about allergies before confirming the order.
- Mention that prices exclude tax.
- Do not accept payment information in chat.
- If a requested item is unavailable, suggest the closest listed menu item.
- End with a concise order summary.
""",
        "config.yaml": "endpoint: http://127.0.0.1:8000/v1\nmodel: local-model\n",
    }


def _local_doc_qa_files() -> dict[str, str]:
    return {
        "README.md": _base_readme(
            "Local Document Q&A",
            "A small document question-answering starter with keyword retrieval fallback.",
            "python ingest.py && python query.py",
        ),
        "ingest.py": r'''from __future__ import annotations

from pathlib import Path

DOCS = Path("docs")
INDEX = Path("index.txt")


def main() -> None:
    chunks = []
    for path in sorted(DOCS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        chunks.append("# " + path.name + "\n" + text.strip())
    INDEX.write_text("\n\n---\n\n".join(chunks), encoding="utf-8")
    print("Indexed {0} Markdown file(s) into {1}".format(len(chunks), INDEX))


if __name__ == "__main__":
    main()
''',
        "query.py": r'''from __future__ import annotations

from pathlib import Path

INDEX = Path("index.txt")


def score(text: str, question: str) -> int:
    terms = {term.lower().strip(".,?!") for term in question.split() if len(term) > 2}
    lowered = text.lower()
    return sum(1 for term in terms if term in lowered)


def main() -> None:
    if not INDEX.exists():
        print("Run python ingest.py first.")
        return
    chunks = [chunk for chunk in INDEX.read_text(encoding="utf-8").split("\n\n---\n\n") if chunk.strip()]
    question = input("question> ").strip()
    ranked = sorted(chunks, key=lambda chunk: score(chunk, question), reverse=True)
    print("\nTop local context matches:\n")
    for index, chunk in enumerate(ranked[:3], start=1):
        print("[{0}]".format(index))
        print(chunk[:1200])
        print()
    if not ranked:
        print("No documents indexed.")
    print("Next: send this context to your configured local OpenAI-compatible endpoint.")


if __name__ == "__main__":
    main()
''',
        "requirements.txt": "# Standard library only. Add packages here if you extend the demo.\n",
        "docs/sample.md": """# Sample Local Document

InferDoctor helps diagnose local AI stacks and guide setup steps.

Use `inferdoctor` for a health dashboard, `inferdoctor recommend` for stack guidance, and `inferdoctor template list` for starter ideas.
""",
        "config.yaml": "endpoint: http://127.0.0.1:8000/v1\nmodel: local-model\nretrieval: keyword\n",
    }


TEMPLATE_FILE_BUILDERS = {
    "customer-service": _customer_service_files,
    "restaurant-ordering": _restaurant_ordering_files,
    "local-doc-qa": _local_doc_qa_files,
}


def create_template_project(name: str, output_dir: str) -> list[str]:
    get_template(name)
    if name not in TEMPLATE_FILE_BUILDERS:
        available = ", ".join(sorted(TEMPLATE_FILE_BUILDERS))
        raise KeyError("template '{0}' is catalog-only for now. Creatable templates: {1}".format(name, available))
    root = Path(output_dir).expanduser()
    files = TEMPLATE_FILE_BUILDERS[name]()
    written: list[str] = []
    for relative, content in files.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        written.append(str(destination))
    return written


def render_template_create_summary(name: str, output_dir: str, written: list[str]) -> str:
    run_command = "python app.py" if name in {"customer-service", "restaurant-ordering"} else "python ingest.py && python query.py"
    lines = [
        "InferDoctor Starter Project Created",
        "=" * 57,
        "Template: {0}".format(name),
        "Output directory: {0}".format(output_dir),
        "",
        "Generated files:",
    ]
    lines.extend("  - {0}".format(path) for path in written)
    lines.extend([
        "",
        "What to do next:",
        "  1. cd {0}".format(output_dir),
        "  2. Edit .env.example or config.yaml for your local endpoint.",
        "  3. {0}".format(run_command),
        "",
        "Endpoint examples:",
        "  Ollama OpenAI-compatible: http://127.0.0.1:11434/v1",
        "  LM Studio: http://127.0.0.1:1234/v1",
        "  vLLM: http://127.0.0.1:8000/v1",
        "  SGLang: http://127.0.0.1:30000/v1",
        "",
        "If the app cannot connect, diagnose the endpoint first:",
        "  inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1",
        "  inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1",
    ])
    return "\n".join(lines)
