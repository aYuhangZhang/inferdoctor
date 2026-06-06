from __future__ import annotations

import subprocess
from typing import List


def run_command(args: List[str], timeout: float = 5.0) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        check=False,
        text=True,
        timeout=timeout,
    )
