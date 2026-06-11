from __future__ import annotations

import json
from textwrap import shorten
from typing import Iterable, List

from inferdoctor.core.config import Config
from inferdoctor.core.health import calculate_health, recommend_fixes
from inferdoctor.core.models import CheckResult


DISPLAY_NAMES = {
    "system": "System",
    "nvidia": "NVIDIA",
    "cuda": "CUDA",
    "ollama": "Ollama",
    "vllm": "vLLM",
    "sglang": "SGLang",
    "xinference": "Xinference",
    "dify": "Dify",
}


def render_console(
    results: Iterable[CheckResult], verbose: bool = False
) -> str:
    lines = []
    for result in results:
        lines.append(
            "[{0:<4}] {1:<10} {2}".format(
                result.status.value.upper(), result.name, result.summary
            )
        )
        for detail in result.details:
            lines.append("       - {0}".format(detail))
        for suggestion in result.suggestions:
            lines.append("       suggestion: {0}".format(suggestion))
        if verbose:
            raw_data = json.dumps(result.raw_data, indent=2, sort_keys=True)
            lines.append("       raw_data:")
            lines.extend(
                "         {0}".format(line) for line in raw_data.splitlines()
            )
    return "\n".join(lines)


def render_dashboard(
    results: Iterable[CheckResult], config: Config, verbose: bool = False
) -> str:
    result_list = list(results)
    health = calculate_health(result_list)
    lines: List[str] = [
        "InferDoctor - Local AI Stack Health Check",
        "=" * 57,
        "Overall Health: {0} / 100  ({1})".format(health.score, health.label),
        "PASS 100 | WARN 60 | FAIL 0 | SKIP 85  (heuristic)",
        "",
        "Component   Status   Summary",
        "----------- -------- --------------------------------------------------",
    ]
    for result in result_list:
        lines.append(
            "{0:<11} {1:<8} {2}".format(
                DISPLAY_NAMES.get(result.name, result.name.title()),
                result.status.value.upper(),
                shorten(result.summary, width=50, placeholder="..."),
            )
        )

    fixes = recommend_fixes(result_list, config)
    lines.extend(["", "Top recommended fixes:"])
    if not fixes:
        lines.append("No immediate fixes recommended. Your detected stack looks healthy.")
    for index, fix in enumerate(fixes, start=1):
        lines.extend(
            [
                "{0}. {1}: {2}".format(index, fix.component, fix.issue),
                "   Likely cause: {0}".format(fix.likely_cause),
                "   Try: {0}".format(fix.next_command),
            ]
        )
        if fix.config_hint:
            hint_label = (
                "Config" if fix.config_hint.startswith("endpoints.") else "Note"
            )
            lines.append(
                "   {0}: {1}".format(hint_label, fix.config_hint)
            )

    if verbose:
        lines.extend(["", "Detailed diagnostics:", render_console(result_list, True)])
    return "\n".join(lines)
