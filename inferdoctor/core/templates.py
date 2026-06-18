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
        generated_files_planned=["README.md", "app.py", "requirements.txt", ".env.example", "data/faq.md", "config.yaml", "prompts/system_prompt.md", "troubleshooting.md"],
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
        generated_files_planned=["README.md", "app.py", "requirements.txt", ".env.example", "data/menu.yaml", "data/policies.md", "config.yaml", "prompts/system_prompt.md", "examples/sample_orders.md", "troubleshooting.md"],
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
        generated_files_planned=["README.md", "ingest.py", "query.py", "requirements.txt", ".env.example", "docs/sample.md", "config.yaml", "troubleshooting.md"],
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

ENDPOINT_EXAMPLES = [
    ("Ollama OpenAI-compatible", "http://127.0.0.1:11434/v1"),
    ("LM Studio", "http://127.0.0.1:1234/v1"),
    ("vLLM", "http://127.0.0.1:8000/v1"),
    ("SGLang", "http://127.0.0.1:30000/v1"),
    ("Xinference OpenAI-compatible", "http://127.0.0.1:9997/v1"),
]


APP_CLIENT = r"""from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "__DEFAULT_ENDPOINT__"
DEFAULT_MODEL = "local-model"
ROOT = Path(__file__).resolve().parent


def read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def read_simple_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_settings() -> tuple[str, str, int]:
    env_file = read_env_file(ROOT / ".env")
    config = read_simple_config(ROOT / "config.yaml")
    base_url = os.environ.get("LOCAL_AI_BASE_URL") or env_file.get("LOCAL_AI_BASE_URL") or config.get("endpoint") or DEFAULT_BASE_URL
    model = os.environ.get("LOCAL_AI_MODEL") or env_file.get("LOCAL_AI_MODEL") or config.get("model") or DEFAULT_MODEL
    timeout_text = os.environ.get("LOCAL_AI_TIMEOUT") or env_file.get("LOCAL_AI_TIMEOUT") or config.get("timeout") or "30"
    try:
        timeout = int(timeout_text)
    except ValueError:
        timeout = 30
    return base_url.rstrip("/"), model, timeout


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_context() -> str:
__DATA_LOADER__


def load_system_prompt() -> str:
    prompt_path = ROOT / "prompts" / "system_prompt.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8").strip()
    return "__SYSTEM_PROMPT__"


def ask_local_model(message: str) -> str:
    base_url, model, timeout = load_settings()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": load_system_prompt() + "\n\nContext:\n" + load_context()},
            {"role": "user", "content": message},
        ],
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        base_url + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return "Endpoint returned HTTP {0}. Check base URL, model name, and whether auth is required.".format(exc.code)
    except urllib.error.URLError as exc:
        return "Could not reach local endpoint. Check LOCAL_AI_BASE_URL or config.yaml. Details: {0}".format(exc.reason)
    except json.JSONDecodeError:
        return "Endpoint responded, but the response was not valid JSON. Verify OpenAI-compatible mode."

    try:
        return body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return "Endpoint response did not look like OpenAI chat completions JSON."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a local OpenAI-compatible starter chat loop. No cloud API key is required by default."
    )
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="Print resolved endpoint/model settings and exit without calling the model",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show prompt, local context, and endpoint settings without calling the model",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    base_url, model, timeout = load_settings()
    if args.check_config:
        print("Endpoint: {0}".format(base_url))
        print("Model: {0}".format(model))
        print("Timeout: {0}s".format(timeout))
        print("No endpoint call was made.")
        return
    if args.dry_run:
        print("Dry run: no endpoint call was made.")
        print("Endpoint: {0}".format(base_url))
        print("Model: {0}".format(model))
        print("Timeout: {0}s".format(timeout))
        print("System prompt preview:")
        print(load_system_prompt()[:600])
        print("Context preview:")
        print(load_context()[:1000])
        print("Next: run python app.py when your local endpoint is ready.")
        return
    print("Local AI starter connected to {0} with model '{1}'.".format(base_url, model))
    print("Type 'exit' to quit. No cloud API key is required by default.")
    while True:
        try:
            message = input("you> ").strip()
        except EOFError:
            break
        if message.lower() in {"exit", "quit"}:
            break
        if not message:
            continue
        print("assistant> " + ask_local_model(message))


if __name__ == "__main__":
    main()
"""


def _endpoint_examples_markdown() -> str:
    return "\n".join("- {0}: `{1}`".format(name, url) for name, url in ENDPOINT_EXAMPLES)


def _help_command(command: str) -> str:
    return "python query.py --help" if "query.py" in command else "python app.py --help"


def _dry_run_command(command: str) -> str:
    return "python query.py --dry-run" if "query.py" in command else "python app.py --dry-run"


def _check_config_command(command: str) -> str:
    return "python query.py --check-config" if "query.py" in command else "python app.py --check-config"


def _base_readme(title: str, purpose: str, command: str, extra: str = "") -> str:
    return """# {title}

{purpose}

This starter is generated by InferDoctor for a local OpenAI-compatible endpoint.
It does not require a cloud API key by default and does not download or run models for you.

## Quick Start

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
inferdoctor template validate .
inferdoctor template smoke-test .
{help_command}
{dry_run_command}
{check_config_command}
{command}
```

## Expected File Tree

```text
.
├── README.md
├── config.yaml
├── .env.example
├── requirements.txt
├── troubleshooting.md
├── app.py or query.py
├── prompts/
└── data/ or docs/
```

## Configure Your Local Endpoint

Edit `.env` or `config.yaml`:

```bash
LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1
LOCAL_AI_MODEL=local-model
LOCAL_AI_TIMEOUT=30
```

Endpoint examples:

{endpoint_examples}

Use whichever runtime you already have running. The app sends requests to `/chat/completions` under that base URL.

## Diagnose Before Running

```bash
inferdoctor
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor explain openai-compatible-connection-refused
```
{extra}

## Validate This Template

```bash
inferdoctor template validate .
inferdoctor template smoke-test .
```

Validation is read-only. Smoke tests only run safe help, dry-run, and config-check commands. They do not install dependencies, call endpoints, or run inference.

## Troubleshooting

See `troubleshooting.md` for common local endpoint problems and fixes.

## Safety

The template sends prompts only to the endpoint you configure. Keep it pointed at a local service if you want a local-only demo.
""".format(
        title=title,
        purpose=purpose,
        command=command,
        help_command=_help_command(command),
        dry_run_command=_dry_run_command(command),
        check_config_command=_check_config_command(command),
        endpoint_examples=_endpoint_examples_markdown(),
        extra=extra,
    )


def _chat_client_py(system_prompt: str, data_loader: str) -> str:
    return (
        APP_CLIENT.replace("__DEFAULT_ENDPOINT__", DEFAULT_ENDPOINT)
        .replace("__SYSTEM_PROMPT__", system_prompt.replace('"', '\\"'))
        .replace("__DATA_LOADER__", data_loader.rstrip())
    )


def _common_troubleshooting() -> str:
    return """# Troubleshooting

## Connection refused

The local AI server is probably not running or the port is wrong.

Try:

```bash
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor check ollama --endpoint http://127.0.0.1:11434
```

## 404 or wrong base URL

Many OpenAI-compatible servers expect the base URL to include `/v1`.

Examples:

- `http://127.0.0.1:8000/v1` for vLLM
- `http://127.0.0.1:30000/v1` for SGLang
- `http://127.0.0.1:1234/v1` for LM Studio
- `http://127.0.0.1:11434/v1` for Ollama OpenAI-compatible mode

## 401 or 403

Your endpoint may require an API key. This starter does not require one by default.
If your local server requires auth, extend `app.py` to add an `Authorization` header.

## Invalid JSON or response shape

The server may not expose OpenAI-compatible chat completions. Run:

```bash
inferdoctor explain openai-compatible-invalid-json
inferdoctor explain openai-compatible-404
```

## Slow responses

Use a smaller model, a quantized model, or a runtime better matched to your hardware.
Run:

```bash
inferdoctor model fit --size 14b --quant q4 --vram 24
inferdoctor recommend --goal customer-service --vram 24
```
"""


def _customer_service_files() -> dict[str, str]:
    data_loader = '    return read_text("data/faq.md")'
    return {
        "README.md": _base_readme(
            "Customer Service Chatbot",
            "A local FAQ assistant for answering product, billing, shipping, warranty, and support questions.",
            "python app.py",
            extra="""
## Try These Prompts

- What is the return policy?
- How long does shipping take?
- Is there a warranty?
- Can support see my password?
""",
        ),
        "app.py": _chat_client_py(
            "You are a concise customer service assistant. Answer only from the FAQ context. If the answer is missing, say you do not know and suggest contacting support.",
            data_loader,
        ),
        "requirements.txt": "# Standard library only. Add packages here if you extend the demo.\n",
        ".env.example": "LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1\nLOCAL_AI_MODEL=local-model\nLOCAL_AI_TIMEOUT=30\n",
        "config.yaml": "endpoint: http://127.0.0.1:8000/v1\nmodel: local-model\ntimeout: 30\n",
        "prompts/system_prompt.md": """You are a concise customer service assistant for Acme Local Shop.

Rules:
- Answer only from the FAQ context.
- If the FAQ does not contain the answer, say you do not know.
- Do not invent policies, prices, or account information.
- Keep answers short and helpful.
- Suggest contacting human support for account-specific issues.
""",
        "data/faq.md": """# Example FAQ

## Shipping
Standard shipping usually takes 3-5 business days. Expedited shipping takes 1-2 business days when available.

## Billing
Invoices are emailed after checkout. Customers can update billing details before an order ships, but payment card numbers are never shown to support agents.

## Returns
Unused items can be returned within 30 days with the original receipt. Opened software, personalized items, and gift cards are not refundable.

## Warranty
Hardware accessories include a one-year limited warranty against manufacturing defects. The warranty does not cover accidental damage or normal wear.

## Account Help
Customers can reset their password from the sign-in page. Support cannot view, recover, or share passwords.

## Support Hours
Support is available Monday to Friday, 09:00-18:00 local time. Urgent outage reports are monitored after hours.
""",
        "troubleshooting.md": _common_troubleshooting(),
    }


def _restaurant_ordering_files() -> dict[str, str]:
    data_loader = '    return read_text("data/menu.yaml") + "\\n\\n" + read_text("data/policies.md")'
    return {
        "README.md": _base_readme(
            "Restaurant Ordering Assistant",
            "A local restaurant ordering assistant with menu data, ordering policy, examples, and local endpoint configuration.",
            "python app.py",
            extra="""
## Try These Prompts

- I want a spicy ramen and a drink.
- What vegetarian options do you have?
- Build an order for two people under 30 dollars.
- I have a soy allergy. What should I avoid?
""",
        ),
        "app.py": _chat_client_py(
            "You are a restaurant ordering assistant. Help users choose items, clarify options, ask about allergies, and follow the ordering policies. Do not invent unavailable menu items or take payment details.",
            data_loader,
        ),
        "requirements.txt": "# Standard library only. Add packages here if you extend the demo.\n",
        ".env.example": "LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1\nLOCAL_AI_MODEL=local-model\nLOCAL_AI_TIMEOUT=30\n",
        "config.yaml": "endpoint: http://127.0.0.1:8000/v1\nmodel: local-model\ntimeout: 30\n",
        "prompts/system_prompt.md": """You are a local restaurant ordering assistant.

Rules:
- Use only the menu and policies provided.
- Ask about pickup or dine-in before finalizing.
- Ask about allergies before confirming an order.
- Do not accept payment information in chat.
- End with a concise order summary.
""",
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
  - name: Chicken Karaage
    price: 8
    options: [regular, spicy mayo]
    allergens: [wheat, egg]
  - name: Gyoza
    price: 6
    options: [pork, vegetable]
    allergens: [wheat, soy]
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
        "examples/sample_orders.md": """# Sample Orders

## Quick lunch
User: I want something vegetarian and not too expensive.
Assistant should suggest the Vegetable Rice Bowl and ask about size and allergies.

## Ramen order
User: I want spicy ramen and gyoza for pickup.
Assistant should confirm spice level, gyoza type, pickup, allergies, and summarize the order.
""",
        "troubleshooting.md": _common_troubleshooting(),
    }


def _local_doc_qa_files() -> dict[str, str]:
    return {
        "README.md": _base_readme(
            "Local Document Q&A",
            "A small document question-answering starter with simple Markdown ingestion and keyword retrieval fallback. It does not require a vector database.",
            "python ingest.py && python query.py --dry-run",
            extra="""
## How It Works

1. Put Markdown files in `docs/`.
2. Run `python ingest.py` to build a plain-text local index.
3. Run `python query.py` to find relevant local context.
4. Run `python query.py --dry-run` or `python query.py --check-config` before using a live endpoint.
5. Use the printed context with your local endpoint, or extend `query.py` to call `/chat/completions`.
""",
        ),
        "ingest.py": """from __future__ import annotations

import argparse
from pathlib import Path

DOCS = Path("docs")
INDEX = Path("index.txt")


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Build a plain-text keyword index from Markdown files in docs/.")


def main() -> None:
    build_parser().parse_args()
    chunks = []
    for path in sorted(DOCS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        chunks.append("# " + path.name + "\\n" + text.strip())
    INDEX.write_text("\\n\\n---\\n\\n".join(chunks), encoding="utf-8")
    print("Indexed {0} Markdown file(s) into {1}".format(len(chunks), INDEX))


if __name__ == "__main__":
    main()
""",
        "query.py": """from __future__ import annotations

import argparse
import os
from pathlib import Path

INDEX = Path("index.txt")
CONFIG = Path("config.yaml")
ENV_FILE = Path(".env")
DEFAULT_BASE_URL = "http://127.0.0.1:8000/v1"
DEFAULT_MODEL = "local-model"


def read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def read_simple_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_settings() -> tuple[str, str, str]:
    env_file = read_env_file(ENV_FILE)
    config = read_simple_config(CONFIG)
    base_url = os.environ.get("LOCAL_AI_BASE_URL") or env_file.get("LOCAL_AI_BASE_URL") or config.get("endpoint") or DEFAULT_BASE_URL
    model = os.environ.get("LOCAL_AI_MODEL") or env_file.get("LOCAL_AI_MODEL") or config.get("model") or DEFAULT_MODEL
    retrieval = config.get("retrieval") or "keyword"
    return base_url.rstrip("/"), model, retrieval


def tokenize(text: str) -> set[str]:
    return {term.lower().strip(".,?!:;()[]{}") for term in text.split() if len(term) > 2}


def score(text: str, question: str) -> int:
    terms = tokenize(question)
    lowered = text.lower()
    return sum(1 for term in terms if term in lowered)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search the local keyword index and print the most relevant Markdown chunks."
    )
    parser.add_argument("question", nargs="?", help="Question to search for; omit for interactive prompt")
    parser.add_argument("--check-config", action="store_true", help="Print endpoint/model/retrieval settings and exit")
    parser.add_argument("--dry-run", action="store_true", help="Show a safe retrieval preview without calling a model endpoint")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    base_url, model, retrieval = load_settings()
    if args.check_config:
        print("Endpoint: {0}".format(base_url))
        print("Model: {0}".format(model))
        print("Retrieval: {0}".format(retrieval))
        print("No endpoint call was made.")
        return
    if args.dry_run:
        print("Dry run: no endpoint call was made.")
        print("Endpoint: {0}".format(base_url))
        print("Model: {0}".format(model))
        print("Retrieval: {0}".format(retrieval))
        if INDEX.exists():
            chunks = [chunk for chunk in INDEX.read_text(encoding="utf-8").split("\\n\\n---\\n\\n") if chunk.strip()]
            print("Indexed chunks: {0}".format(len(chunks)))
            if chunks:
                print("Context preview:")
                print(chunks[0][:1000])
        else:
            print("Index is missing. Run python ingest.py before real queries.")
        print("Next: run python ingest.py, then python query.py 'your question'.")
        return
    if not INDEX.exists():
        print("Run python ingest.py first.")
        return
    chunks = [chunk for chunk in INDEX.read_text(encoding="utf-8").split("\\n\\n---\\n\\n") if chunk.strip()]
    question = args.question or input("question> ").strip()
    ranked = sorted(chunks, key=lambda chunk: score(chunk, question), reverse=True)
    print("\\nTop local context matches:\\n")
    for index, chunk in enumerate(ranked[:3], start=1):
        print("[{0}] score={1}".format(index, score(chunk, question)))
        print(chunk[:1200])
        print()
    if not ranked:
        print("No documents indexed.")
    print("Next: send this context to your configured local OpenAI-compatible endpoint.")
    print("Tip: run inferdoctor check vllm or inferdoctor check sglang if the endpoint fails.")


if __name__ == "__main__":
    main()
""",
        "requirements.txt": "# Standard library only. Add packages here if you extend the demo.\n",
        ".env.example": "LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1\nLOCAL_AI_MODEL=local-model\nLOCAL_AI_TIMEOUT=30\n",
        "config.yaml": "endpoint: http://127.0.0.1:8000/v1\nmodel: local-model\ntimeout: 30\nretrieval: keyword\n",
        "docs/sample.md": """# Sample Local Document

InferDoctor helps diagnose local AI stacks and guide setup steps.

Use `inferdoctor` for a health dashboard, `inferdoctor recommend` for stack guidance, and `inferdoctor template list` for starter ideas.

## Local AI Terms

An OpenAI-compatible endpoint usually exposes `/v1/models` and `/v1/chat/completions`.
Ollama, LM Studio, vLLM, SGLang, and Xinference can be used as local model backends depending on your setup.
""",
        "troubleshooting.md": _common_troubleshooting(),
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
    run_command = "python app.py" if name in {"customer-service", "restaurant-ordering"} else "python ingest.py && python query.py \"What is an OpenAI-compatible endpoint?\""
    dry_run_command = "python app.py --dry-run" if name in {"customer-service", "restaurant-ordering"} else "python query.py --dry-run"
    check_config_command = "python app.py --check-config" if name in {"customer-service", "restaurant-ordering"} else "python query.py --check-config"
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
        "  2. cp .env.example .env",
        "  3. Validate the generated project: inferdoctor template validate {0}".format(output_dir),
        "  4. Smoke-test the project without calling a model: inferdoctor template smoke-test {0}".format(output_dir),
        "  5. Edit .env or config.yaml for your local endpoint.",
        "  6. Try safe generated commands before using a live endpoint:",
        "     {0}".format(dry_run_command),
        "     {0}".format(check_config_command),
        "  7. {0}".format(run_command),
        "",
        "Endpoint examples:",
    ])
    lines.extend("  {0}: {1}".format(name, url) for name, url in ENDPOINT_EXAMPLES)
    lines.extend([
        "",
        "If the app cannot connect, diagnose the endpoint first:",
        "  inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1",
        "  inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1",
        "  inferdoctor explain openai-compatible-connection-refused",
    ])
    return "\n".join(lines)
