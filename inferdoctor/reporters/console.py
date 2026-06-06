from __future__ import annotations

import json
from typing import Iterable

from inferdoctor.core.models import CheckResult


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
