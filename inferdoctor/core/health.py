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
    impact: Optional[str] = None


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


def _status_impact(status: Status, service_name: str) -> str:
    if status == Status.FAIL:
        return "Likely blocking for this component until fixed."
    if status == Status.WARN:
        return "Needs attention if your app depends on {0}.".format(service_name)
    return "Optional unless {0} is part of your local stack.".format(service_name)


def _endpoint_fix(result: CheckResult, config: Config) -> RecommendedFix:
    endpoint = config.endpoints[result.name]
    label = {
        "vllm": "vLLM",
        "sglang": "SGLang",
        "llamacpp": "llama.cpp",
        "lmstudio": "LM Studio",
        "xinference": "Xinference",
        "dify": "Dify",
        "openwebui": "Open WebUI",
        "ollama": "Ollama",
    }[result.name]
    summary = result.summary.lower()
    if "404" in summary:
        cause = (
            "The service responded, but /v1/models was not found. The base URL "
            "may be missing or duplicating /v1."
        )
    elif "authentication" in summary or "unauthorized" in summary:
        cause = "The endpoint requires authentication or the proxy blocks this route."
    elif "invalid json" in summary or "not openai-compatible" in summary:
        cause = "The URL may point to a web UI or a non-compatible API route."
    elif result.name == "dify":
        cause = (
            "Dify is optional. If you run it locally, the service may be stopped "
            "or mapped to another port."
        )
    else:
        cause = "The service may not be running, or it may be listening on another port."

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
        impact=_status_impact(result.status, label),
    )


def _fix_for(
    result: CheckResult, config: Config, by_name: Dict[str, CheckResult]
) -> RecommendedFix:
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
            impact="Required only for NVIDIA GPU inference or CUDA-backed runtimes.",
        )
    if result.name == "cuda":
        nvidia = by_name.get("nvidia")
        driver_available = nvidia is not None and nvidia.status == Status.PASS
        cause = (
            "NVIDIA driver is available, but CUDA toolkit was not found. This "
            "may be OK if you only use prebuilt runtimes such as Ollama."
            if driver_available
            else "The CUDA toolkit is absent or nvcc is not on PATH."
        )
        return RecommendedFix(
            component="CUDA",
            issue=result.summary,
            likely_cause=cause,
            next_command="nvcc --version",
            config_hint=(
                "Install CUDA toolkit only if you need to compile CUDA workloads "
                "or use runtimes that require nvcc."
            ),
            impact="Optional for CPU-only and many prebuilt runtimes; required for CUDA compilation.",
        )
    if result.name == "docker":
        return RecommendedFix(
            component="Docker",
            issue=result.summary,
            likely_cause=(
                "The Docker CLI is missing, the daemon is stopped, or the current "
                "user cannot reach the Docker daemon."
            ),
            next_command="docker info",
            config_hint="InferDoctor only checks Docker status; it never starts containers.",
            impact="Required only if your local AI stack runs services in containers.",
        )
    return RecommendedFix(
        component=result.name.title(),
        issue=result.summary,
        likely_cause="The diagnostic could not confirm this component is healthy.",
        next_command="inferdoctor check {0} --verbose".format(result.name),
        impact="Review this component if it is part of your local AI stack.",
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
        "llamacpp": 3,
        "lmstudio": 4,
        "dify": 5,
        "xinference": 6,
        "openwebui": 7,
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
        _fix_for(result, config, by_name) for result in candidates[:effective_limit]
    ]
