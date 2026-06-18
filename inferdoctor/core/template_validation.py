from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import List


@dataclass(frozen=True)
class TemplateValidationItem:
    name: str
    status: str
    summary: str
    fix: str = ""


@dataclass(frozen=True)
class TemplateValidationReport:
    path: Path
    template_type: str
    items: List[TemplateValidationItem]

    @property
    def status(self) -> str:
        if any(item.status == "FAIL" for item in self.items):
            return "FAIL"
        if any(item.status == "WARN" for item in self.items):
            return "WARN"
        return "PASS"


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _detect_template_type(root: Path) -> str:
    readme = _read_text(root / "README.md").lower()
    config = _read_text(root / "config.yaml").lower()
    combined = readme + "\n" + config
    if (root / "data" / "faq.md").exists() or "customer service" in combined:
        return "customer-service"
    if (root / "data" / "menu.yaml").exists() or "restaurant ordering" in combined:
        return "restaurant-ordering"
    if ((root / "query.py").exists() and (root / "docs").exists()) or "local document q&a" in combined or "retrieval: keyword" in config:
        return "local-doc-qa"
    return "unknown"


def _has_entrypoint(root: Path) -> bool:
    return any((root / relative).exists() for relative in ("app.py", "query.py", "ingest.py"))


def _has_sample_data(root: Path) -> bool:
    return any(
        (root / relative).exists()
        for relative in (
            "data/faq.md",
            "data/menu.yaml",
            "data/policies.md",
            "docs/sample.md",
        )
    )


def _contains_endpoint_config(root: Path) -> bool:
    config = _read_text(root / "config.yaml")
    env_example = _read_text(root / ".env.example")
    return any(
        marker in (config + "\n" + env_example)
        for marker in ("LOCAL_AI_BASE_URL", "endpoint:", "/v1")
    )


SECRET_VALUE_RE = re.compile(
    r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?([a-z0-9_./+\-]{12,})"
)
BEARER_RE = re.compile(r"(?i)bearer\s+[a-z0-9_./+\-]{12,}")


def _secret_hits(root: Path) -> list[str]:
    suspicious_names = (".env", "config.yaml", ".env.example")
    hits: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.name == "__pycache__":
            continue
        if path.suffix not in {".py", ".md", ".yaml", ".yml", ".txt", ".example"} and path.name not in suspicious_names:
            continue
        text = _read_text(path)
        if SECRET_VALUE_RE.search(text) or BEARER_RE.search(text):
            hits.append(str(path.relative_to(root)))
    return sorted(set(hits))


def validate_template_project(path: str) -> TemplateValidationReport:
    root = Path(path).expanduser()
    items: list[TemplateValidationItem] = []
    if not root.exists():
        return TemplateValidationReport(
            path=root,
            template_type="missing",
            items=[TemplateValidationItem("project directory", "FAIL", "Directory does not exist.", "Create a template project first.")],
        )
    if not root.is_dir():
        return TemplateValidationReport(
            path=root,
            template_type="invalid",
            items=[TemplateValidationItem("project directory", "FAIL", "Path is not a directory.", "Pass the generated template directory.")],
        )

    template_type = _detect_template_type(root)
    required_common = ["README.md", "requirements.txt", "config.yaml", ".env.example"]
    for relative in required_common:
        exists = (root / relative).exists()
        items.append(
            TemplateValidationItem(
                relative,
                "PASS" if exists else "FAIL",
                "Found {0}.".format(relative) if exists else "Missing {0}.".format(relative),
                "Regenerate the template or add {0}.".format(relative),
            )
        )

    if _contains_endpoint_config(root):
        items.append(TemplateValidationItem("endpoint config", "PASS", "Local endpoint configuration is present."))
    else:
        items.append(TemplateValidationItem("endpoint config", "FAIL", "No local endpoint configuration found.", "Add LOCAL_AI_BASE_URL to .env or endpoint: to config.yaml."))

    if template_type in {"customer-service", "restaurant-ordering"}:
        has_app = (root / "app.py").exists()
        items.append(TemplateValidationItem("app.py", "PASS" if has_app else "FAIL", "Found CLI app." if has_app else "Missing app.py.", "Regenerate the template or restore app.py."))
        has_prompt = (root / "prompts" / "system_prompt.md").exists()
        items.append(TemplateValidationItem("system prompt", "PASS" if has_prompt else "WARN", "Found system prompt." if has_prompt else "No system prompt file found.", "Add prompts/system_prompt.md for clearer assistant behavior."))
    elif template_type == "local-doc-qa":
        for relative in ("ingest.py", "query.py", "docs/sample.md"):
            exists = (root / relative).exists()
            items.append(TemplateValidationItem(relative, "PASS" if exists else "FAIL", "Found {0}.".format(relative) if exists else "Missing {0}.".format(relative), "Regenerate the local-doc-qa template."))
    else:
        items.append(TemplateValidationItem("template type", "WARN", "Template type was not recognized.", "Use a project generated by inferdoctor template create."))
        has_entrypoint = _has_entrypoint(root)
        items.append(TemplateValidationItem("app entrypoint", "PASS" if has_entrypoint else "FAIL", "Found an app/query entrypoint." if has_entrypoint else "No app.py, query.py, or ingest.py found.", "Add an app entrypoint or regenerate a supported template."))
        has_sample_data = _has_sample_data(root)
        items.append(TemplateValidationItem("sample data", "PASS" if has_sample_data else "WARN", "Found sample data." if has_sample_data else "No sample data files found.", "Add sample data under data/ or docs/ so users can test the app."))

    if template_type == "customer-service":
        exists = (root / "data" / "faq.md").exists()
        items.append(TemplateValidationItem("sample data", "PASS" if exists else "FAIL", "Found data/faq.md." if exists else "Missing data/faq.md.", "Add FAQ content under data/faq.md."))
    if template_type == "restaurant-ordering":
        exists = (root / "data" / "menu.yaml").exists() and (root / "data" / "policies.md").exists()
        items.append(TemplateValidationItem("sample data", "PASS" if exists else "FAIL", "Found menu and policy data." if exists else "Missing menu or policy data.", "Add data/menu.yaml and data/policies.md."))

    secret_hits = _secret_hits(root)
    if secret_hits:
        items.append(TemplateValidationItem("secret scan", "WARN", "Suspicious secret-like text found in: {0}".format(", ".join(secret_hits[:5])), "Remove real keys/tokens before sharing or committing."))
    else:
        items.append(TemplateValidationItem("secret scan", "PASS", "No obvious secrets found in text files."))

    return TemplateValidationReport(path=root, template_type=template_type, items=items)


def render_template_validation(report: TemplateValidationReport) -> str:
    lines = [
        "InferDoctor Template Validation",
        "=" * 57,
        "Path: {0}".format(report.path),
        "Detected template: {0}".format(report.template_type),
        "Overall status: {0}".format(report.status),
        "",
        "Checks:",
    ]
    for item in report.items:
        lines.append("  {0:<18} {1:<4} {2}".format(item.name, item.status, item.summary))
    fixes = [item for item in report.items if item.status in {"WARN", "FAIL"} and item.fix]
    lines.extend(["", "Top fixes:"])
    if fixes:
        for index, item in enumerate(fixes[:3], start=1):
            lines.append("  {0}. {1}: {2}".format(index, item.name, item.fix))
    else:
        lines.append("  1. No fixes needed. Configure .env if you want to use a different local endpoint.")
    if report.template_type in {"customer-service", "restaurant-ordering"}:
        next_command = "  python app.py --help"
    elif report.template_type == "local-doc-qa":
        next_command = "  python ingest.py --help && python query.py --help"
    else:
        next_command = "  inferdoctor template list"
    lines.extend([
        "",
        "Next command to try:",
        "  cd {0}".format(report.path),
        next_command,
        "",
        "Supported layouts: customer-service, restaurant-ordering, local-doc-qa.",
        "This validation is read-only. It does not install dependencies, call endpoints, or run inference.",
    ])
    return "\n".join(lines)
