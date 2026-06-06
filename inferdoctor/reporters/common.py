from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable

from inferdoctor import __version__
from inferdoctor.core.models import CheckResult


def report_document(results: Iterable[CheckResult]) -> Dict[str, Any]:
    return {
        "tool": "InferDoctor",
        "version": __version__,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": [result.to_dict() for result in results],
    }
