from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Sequence

from inferdoctor import __version__
from inferdoctor.checkers import default_registry
from inferdoctor.core.config import ConfigError, load_config
from inferdoctor.core.models import CheckResult, Status
from inferdoctor.core.runner import run_checks
from inferdoctor.reporters import render_console, render_json, render_markdown


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inferdoctor",
        description="Diagnose your local AI inference stack in one command.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")

    check = subparsers.add_parser("check", help="Run diagnostic checks")
    check.add_argument(
        "target",
        nargs="?",
        choices=default_registry().names(),
        help="Run one checker; omit to run all checks",
    )
    check.add_argument("--config", help="Path to a JSON or simple YAML config")

    report = subparsers.add_parser("report", help="Generate a diagnostic report")
    report.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Report output format",
    )
    report.add_argument("--output", help="Write the report to this file")
    report.add_argument("--config", help="Path to a JSON or simple YAML config")
    return parser


def _load(path: Optional[str]):
    try:
        return load_config(path)
    except ConfigError as exc:
        raise SystemExit("inferdoctor: configuration error: {0}".format(exc))


def _results_for_target(target: Optional[str], config_path: Optional[str]):
    registry = default_registry()
    checkers = [registry.get(target)] if target else registry.all()
    return run_checks(checkers, _load(config_path))


def _exit_code(results: List[CheckResult]) -> int:
    return 1 if any(result.status == Status.FAIL for result in results) else 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    results = _results_for_target(
        getattr(args, "target", None), getattr(args, "config", None)
    )
    if args.command == "check":
        print(render_console(results))
        return _exit_code(results)

    rendered = (
        render_json(results)
        if args.format == "json"
        else render_markdown(results)
    )
    if args.output:
        try:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        except OSError as exc:
            print("inferdoctor: could not write report: {0}".format(exc), file=sys.stderr)
            return 2
    else:
        print(rendered)
    return _exit_code(results)
