from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from inferdoctor import __version__
from inferdoctor.checkers import default_registry
from inferdoctor.core.capacity import render_capacity
from inferdoctor.core.config import (
    Config,
    ConfigError,
    load_config,
    normalize_endpoint,
)
from inferdoctor.core.explain import explain_topics, render_explanation
from inferdoctor.core.models import CheckResult, Status
from inferdoctor.core.runner import run_checks
from inferdoctor.reporters import render_dashboard, render_json, render_markdown


def _positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def _add_runtime_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", help="Path to a JSON or simple YAML config")
    parser.add_argument(
        "--timeout",
        type=_positive_float,
        help="HTTP timeout in seconds; overrides the config value",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include raw diagnostic data in console or Markdown output",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inferdoctor",
        description="Find out why your local AI inference stack is not working.",
        epilog="Run 'inferdoctor' for an immediate health score and top fixes.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")

    check = subparsers.add_parser(
        "check",
        help="Check the whole stack or one component",
        description="Check local AI components without installing or running them.",
        epilog=(
            "Examples: inferdoctor check | inferdoctor check sglang "
            "--endpoint http://127.0.0.1:30000/v1"
        ),
    )
    check.add_argument(
        "target",
        nargs="?",
        choices=default_registry().names(),
        help="Component to check; omit to diagnose the full stack",
    )
    check.add_argument(
        "--endpoint",
        help="Override the selected service endpoint for this check",
    )
    _add_runtime_options(check)

    report = subparsers.add_parser(
        "report",
        help="Generate a JSON or Markdown diagnostic report",
        description="Run all checks and create a shareable diagnostic report.",
    )
    report.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Report output format",
    )
    report.add_argument("--output", help="Write the report to this file")
    _add_runtime_options(report)

    explain = subparsers.add_parser(
        "explain",
        help="Explain a common local AI failure",
        description="Show a short troubleshooting guide for a known InferDoctor topic.",
    )
    explain.add_argument(
        "topic",
        choices=explain_topics(),
        help="Troubleshooting topic to explain",
    )

    capacity = subparsers.add_parser(
        "capacity",
        help="Preview local AI workload capacity",
        description=(
            "Estimate local AI hardware readiness with lightweight heuristics. "
            "No models are downloaded or run."
        ),
    )
    capacity.add_argument(
        "--vram",
        type=_positive_float,
        help="Override detected NVIDIA VRAM in GiB",
    )
    capacity.add_argument(
        "--gpu",
        help="Optional GPU name to show with --vram",
    )
    return parser


def _load(path: Optional[str]):
    try:
        return load_config(path)
    except ConfigError as exc:
        raise SystemExit(
            "inferdoctor: configuration error: {0}. "
            "Check the path and the documented endpoints/timeout format.".format(exc)
        )


def _results_for_target(
    target: Optional[str],
    config_path: Optional[str],
    timeout: Optional[float] = None,
    endpoint: Optional[str] = None,
) -> Tuple[List[CheckResult], Config]:
    registry = default_registry()
    checkers = [registry.get(target)] if target else registry.all()
    config = _load(config_path)
    if timeout is not None:
        config.timeout = timeout
    if endpoint is not None:
        if target is None:
            raise SystemExit("inferdoctor: --endpoint requires a component name")
        if target not in config.endpoints:
            raise SystemExit(
                "inferdoctor: {0} does not use an HTTP endpoint".format(target)
            )
        try:
            config.endpoints[target] = normalize_endpoint(target, endpoint)
        except ConfigError as exc:
            raise SystemExit("inferdoctor: {0}".format(exc)) from exc
    return run_checks(checkers, config), config


def _exit_code(results: List[CheckResult]) -> int:
    return 1 if any(result.status == Status.FAIL for result in results) else 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _parser()
    arguments = list(argv) if argv is not None else sys.argv[1:]
    if not arguments:
        arguments = ["check"]
    args = parser.parse_args(arguments)

    if args.command == "explain":
        print(render_explanation(args.topic))
        return 0
    if args.command == "capacity":
        print(render_capacity(vram_gib=args.vram, gpu_name=args.gpu))
        return 0

    results, config = _results_for_target(
        getattr(args, "target", None),
        getattr(args, "config", None),
        getattr(args, "timeout", None),
        getattr(args, "endpoint", None),
    )
    if args.command == "check":
        print(render_dashboard(results, config, verbose=args.verbose))
        return _exit_code(results)

    rendered = (
        render_json(results)
        if args.format == "json"
        else render_markdown(results, verbose=args.verbose)
    )
    if args.output:
        try:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        except OSError as exc:
            print(
                "inferdoctor: could not write report to '{0}': {1}. "
                "Check that the parent directory exists and is writable.".format(
                    args.output, exc
                ),
                file=sys.stderr,
            )
            return 2
    else:
        print(rendered)
    return _exit_code(results)
