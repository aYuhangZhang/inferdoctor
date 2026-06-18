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
from inferdoctor.core.profile import render_profile_json, render_profile_markdown
from inferdoctor.core.runner import run_checks
from inferdoctor.core.scenarios import evaluate_scenarios, render_scenarios, scenario_names
from inferdoctor.core.setup import GOALS, PREFERENCES, RUNTIMES, recommend_setup, render_setup_plan
from inferdoctor.core.templates import (
    create_template_project,
    render_template_create_summary,
    render_template_detail,
    render_template_list,
    template_names,
)
from inferdoctor.reporters import render_dashboard, render_json, render_markdown


def _model_size(value: str) -> str:
    stripped = value.strip().lower()
    number = stripped[:-1] if stripped.endswith("b") else stripped
    try:
        parsed = float(number)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a size like 7b, 14b, or 32b") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return stripped if stripped.endswith("b") else "{0:g}b".format(parsed)


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

    profile = subparsers.add_parser(
        "profile",
        help="Generate a safe, redacted diagnostic profile",
        description=(
            "Create a shareable local AI environment profile with secrets, "
            "endpoint credentials, query strings, and home paths redacted."
        ),
    )
    profile.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Profile output format",
    )
    profile.add_argument("--output", help="Write the profile to this file")
    _add_runtime_options(profile)

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

    init = subparsers.add_parser(
        "init",
        help="Get a guided local AI setup recommendation",
        description=(
            "Ask a few lightweight questions and recommend a runtime path, "
            "template, and next commands. No installation is performed."
        ),
    )
    init.add_argument(
        "--goal",
        choices=GOALS,
        help="What you want to build",
    )
    init.add_argument(
        "--preference",
        choices=PREFERENCES,
        help="Optimize for easiest setup, performance, CPU, or GPU",
    )
    init.add_argument(
        "--runtime",
        choices=RUNTIMES,
        help="Local runtime you already have, if known",
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
        help="GPU name to display or infer common VRAM from, for example 'RTX 3090'",
    )
    capacity.add_argument(
        "--model-size",
        type=_model_size,
        help="Optional model size heuristic, for example 7b, 14b, or 32b",
    )
    capacity.add_argument(
        "--quant",
        choices=("q4", "q8"),
        default="q4",
        help="Quantization heuristic to use with --model-size",
    )
    capacity.add_argument(
        "--runtime",
        choices=("ollama", "vllm"),
        help="Runtime heuristic to apply",
    )

    template = subparsers.add_parser(
        "template",
        help="Explore local AI starter templates",
        description=(
            "List and inspect local AI app templates. Template commands do not "
            "download models or install runtimes."
        ),
    )
    template_subparsers = template.add_subparsers(
        dest="template_command", required=True
    )
    template_subparsers.add_parser(
        "list",
        help="List available starter templates",
        description="Show local AI app templates planned for InferDoctor.",
    )
    template_show = template_subparsers.add_parser(
        "show",
        help="Show details for one starter template",
        description="Explain a template's goal, stack, hardware fit, and next command.",
    )
    template_show.add_argument(
        "template",
        choices=template_names(),
        help="Template name to inspect",
    )
    template_create = template_subparsers.add_parser(
        "create",
        help="Create a lightweight starter project",
        description=(
            "Generate a local starter project. This writes files only to the "
            "explicit --output directory and does not install dependencies."
        ),
    )
    template_create.add_argument(
        "template",
        choices=template_names(),
        help="Template name to generate",
    )
    template_create.add_argument(
        "--output",
        required=True,
        help="Directory where the starter project should be written",
    )

    def add_scenario_parser(name: str):
        scenario_parser = subparsers.add_parser(
            name,
            help="Show goal-oriented scenario readiness",
            description="Summarize readiness for common local AI goals using existing checks.",
        )
        scenario_parser.add_argument(
            "target",
            nargs="?",
            choices=scenario_names(),
            help="Scenario to show; omit to show all scenarios",
        )
        _add_runtime_options(scenario_parser)

    add_scenario_parser("scenario")
    add_scenario_parser("scenarios")
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
    if args.command == "init":
        goal = args.goal
        preference = args.preference
        runtime = args.runtime
        interactive = sys.stdin.isatty() and goal is None and preference is None and runtime is None
        if interactive:
            goal = input("What do you want to build? [chatbot/document-qa/customer-service/restaurant-ordering/local-api/not-sure]: ").strip() or None
            preference = input("What do you prefer? [easiest/performance/cpu/gpu]: ").strip() or None
            runtime = input("Existing runtime? [ollama/vllm/sglang/xinference/not-sure]: ").strip() or None
        print(render_setup_plan(recommend_setup(goal, preference, runtime)))
        return 0
    if args.command == "capacity":
        print(
            render_capacity(
                vram_gib=args.vram,
                gpu_name=args.gpu,
                model_size_b=args.model_size,
                quant=args.quant,
                runtime=args.runtime,
            )
        )
        return 0
    if args.command == "template":
        try:
            if args.template_command == "list":
                print(render_template_list())
            elif args.template_command == "show":
                print(render_template_detail(args.template))
            elif args.template_command == "create":
                written = create_template_project(args.template, args.output)
                print(render_template_create_summary(args.template, args.output, written))
        except (KeyError, OSError) as exc:
            print("inferdoctor: {0}".format(exc), file=sys.stderr)
            return 2
        return 0

    if args.command in ("scenario", "scenarios"):
        results, _ = _results_for_target(
            None,
            getattr(args, "config", None),
            getattr(args, "timeout", None),
            None,
        )
        print(render_scenarios(evaluate_scenarios(results, args.target)))
        return _exit_code(results)

    if args.command == "profile":
        results, config = _results_for_target(
            None,
            getattr(args, "config", None),
            getattr(args, "timeout", None),
            None,
        )
        rendered = (
            render_profile_json(results, config)
            if args.format == "json"
            else render_profile_markdown(results, config)
        )
        if args.output:
            try:
                Path(args.output).write_text(rendered + "\n", encoding="utf-8")
            except OSError as exc:
                print(
                    "inferdoctor: could not write profile to '{0}': {1}. "
                    "Check that the parent directory exists and is writable.".format(
                        args.output, exc
                    ),
                    file=sys.stderr,
                )
                return 2
        else:
            print(rendered)
        return _exit_code(results)

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
