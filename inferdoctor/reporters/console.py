from __future__ import annotations

from typing import Iterable

from inferdoctor.core.models import CheckResult


def render_console(results: Iterable[CheckResult]) -> str:
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
    return "\n".join(lines)
