from __future__ import annotations

import json
from typing import Iterable

from inferdoctor.core.models import CheckResult
from inferdoctor.reporters.common import report_document


def render_json(results: Iterable[CheckResult]) -> str:
    return json.dumps(report_document(results), indent=2, sort_keys=True)
