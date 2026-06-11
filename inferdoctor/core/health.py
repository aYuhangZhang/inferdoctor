from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from inferdoctor.core.config import Config
from inferdoctor.core.models import CheckResult, Status


STATUS_SCORES = {
    Status.PASS: 100,
    Status.WARN: 60,
    Status.FAIL: 0,
    Status.SKIP: 85,
}


@dataclass
class HealthSummary:
    score: int
    label: str
    counts: Dict[Status, int]


@dataclass
class RecommendedFix:
    component: str
    issue: str
    likely_cause: str
    next_command: str
    config_hint: Optional[str] = None


def calculate_health(results: Iterable[CheckResult]) -> HealthSummary:
    result_list = list(results)
    counts = {status: 0 for status in Status}
    for result in result_list:
        counts[result.status] += 1
    score = (
        round(
            sum(STATUS_SCORES[result.status] for result in result_list)
            / len(result_list)
        )
        if result_list
        else 0
    )
    if score >= 90:
        label = "Healthy"
    elif score >= 75:
        label = "Mostly healthy"
    elif score >= 50:
        label = "Needs attention"
    else:
        label = "Unhealthy"
    return HealthSummary(score=score, label=label, counts=counts)


def _endpoint_fix(result: CheckResult, config: Config) -> RecommendedFix:
    endpoint = config.endpoints[result.name]
    label = {
        "vllm": "vLLM",
        "sglang": "SGLang",
        "xinference": "Xinference",
        "dify": "Dify",
        "ollama": "Ollama",
    }[result.name]
    summary = result.summary.lower()
    if "404" in summary:
        cause = "The base URL likely has a missing or duplicated /v1 prefix."
    elif "authentication" in summary or "unauthorized" in summary:
        cause = "The server or reverse proxy requires credentials for this route."
    elif "invalid json" in summary or "not openai-compatible" in summary:
        cause = "The URL may point to a web UI or a non-compatible API route."
    else:
        cause = "The service is stopped, listening elsewhere, or the URL is incorrect."

    next_command = "inferdoctor check {0} --endpoint {1}".format(
        result.name, endpoint
    )
    for suggestion in result.suggestions:
        for prefix in ("Try: ", "Retry with: "):
            if suggestion.startswith(prefix):
                next_command = suggestion[len(prefix) :]
                break

    suggested_endpoint = endpoint
    if "--endpoint " in next_command:
        suggested_endpoint = next_command.split("--endpoint ", 1)[1].split()[0]
    return RecommendedFix(
        component=label,
        issue=result.summary,
        likely_cause=cause,
        next_command=next_command,
        config_hint="endpoints.{0}: {1}".format(result.name, suggested_endpoint),
    )


def _fix_for(result: CheckResult, config: Config) -> RecommendedFix:
    if result.name in config.endpoints:
        return _endpoint_fix(result, config)
    if result.name == "nvidia":
        return RecommendedFix(
            component="NVIDIA",
            issue=result.summary,
            likely_cause=(
                "The NVIDIA driver is absent, unhealthy, or nvidia-smi is not "
                "on PATH."
            ),
            next_command="nvidia-smi",
            config_hint="No action is needed on a CPU-only or non-NVIDIA machine.",
        )
    if result.name == "cuda":
        return RecommendedFix(
            component="CUDA",
            issue=result.summary,
            likely_cause=(
                "The CUDA toolkit is absent or nvcc is not on PATH; the NVIDIA "
                "driver may still work."
            ),
            next_command="nvcc --version",
            config_hint=(
                "Prebuilt runtimes may not require nvcc. Install a toolkit only "
                "if your workflow needs it."
            ),
        )
    return RecommendedFix(
        component=result.name.title(),
        issue=result.summary,
        likely_cause="The diagnostic could not confirm this component is healthy.",
        next_command="inferdoctor check {0} --verbose".format(result.name),
    )


def recommend_fixes(
    results: Iterable[CheckResult], config: Config, limit: int = 3
) -> List[RecommendedFix]:
    result_list = list(results)
    by_name = {result.name: result for result in result_list}
    service_order = {
        "vllm": 0,
        "sglang": 1,
        "ollama": 2,
        "dify": 3,
        "xinference": 4,
    }

    def priority(result: CheckResult):
        if result.status == Status.FAIL:
            return (0, 0)
        if result.status == Status.WARN:
            return (1, 0)
        nvidia = by_name.get("nvidia")
        if (
            result.name == "cuda"
            and nvidia is not None
            and nvidia.status == Status.PASS
        ):
            return (2, 0)
        if result.name in service_order:
            return (3, service_order[result.name])
        return (4, 0)

    candidates = [result for result in result_list if result.status != Status.PASS]
    candidates.sort(key=priority)
    required = sum(
        result.status in (Status.FAIL, Status.WARN) for result in candidates
    )
    effective_limit = max(limit, required)
    return [
        _fix_for(result, config) for result in candidates[:effective_limit]
    ]
