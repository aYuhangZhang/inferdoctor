from __future__ import annotations

from collections import OrderedDict
from typing import Dict, Iterable, List

from inferdoctor.core.checker import Checker


class CheckerRegistry:
    def __init__(self, checkers: Iterable[Checker] = ()) -> None:
        self._checkers: Dict[str, Checker] = OrderedDict()
        for checker in checkers:
            self.register(checker)

    def register(self, checker: Checker) -> None:
        if checker.name in self._checkers:
            raise ValueError("Checker already registered: {0}".format(checker.name))
        self._checkers[checker.name] = checker

    def get(self, name: str) -> Checker:
        try:
            return self._checkers[name]
        except KeyError as exc:
            raise KeyError("Unknown checker: {0}".format(name)) from exc

    def names(self) -> List[str]:
        return list(self._checkers)

    def all(self) -> List[Checker]:
        return list(self._checkers.values())
