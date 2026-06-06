from __future__ import annotations

from abc import ABC, abstractmethod

from inferdoctor.core.config import Config
from inferdoctor.core.models import CheckResult


class Checker(ABC):
    name: str

    @abstractmethod
    def run(self, config: Config) -> CheckResult:
        """Run a read-only diagnostic check."""
