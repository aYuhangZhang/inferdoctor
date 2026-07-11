
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from inferdoctor import __version__
from inferdoctor.core.http import HTTPCheckError, describe_http_error, join_url

SMOKE_PROMPT = "Reply with one short sentence: local AI endpoint smoke test."


@dataclass(frozen=True)
class PerfCheck:
    name: str
    status: str
    summary: str
    details: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class PerfResult:
    mode: str
    endpoint: str
    model: Optional[str]
    reachable: bool
    openai_compatible: str
    streaming_supported: str = "unknown"
    ttft_seconds: Optional[float] = None
    total_latency_seconds: Optional[float] = None
    rough_tokens_per_second: Optional[float] = None
    output_tokens_estimate: Optional[int] = None
    user_experience: str = "Inconclusive"
    checks: List[PerfCheck] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)


def _models_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if urlsplit(normalized).path.rstrip("/").endswith("/v1"):
        return join_url(normalized, "models")
    return join_url(normalized, "v1/models")


def _chat_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if urlsplit(normalized).path.rstrip("/").endswith("/v1"):
        return join_url(normalized, "chat/completions")
    return join_url(normalized, "v1/chat/completions")


def _headers() -> Dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "InferDoctor/{0}".format(__version__),
    }


def _read_body(response: Any) -> str:
    return response.read(1024 * 1024).decode("utf-8", errors="replace")


def _http_error_check(url: str, status: int, body: str = "") -> PerfCheck:
    if status in (401, 403):
        return PerfCheck("authentication", "WARN", "Endpoint is reachable but requires authentication.", ["HTTP {0} from {1}".format(status, url)])
    if status == 404:
        return PerfCheck("route", "WARN", "Route returned HTTP 404. The base URL may be missing or duplicating /v1.", ["Probe URL: {0}".format(url)])
    return PerfCheck("http", "WARN", "Endpoint returned HTTP {0}.".format(status), ["Probe URL: {0}".format(url), body[:200] if body else "No response body captured."])


def _get_json(url: str, timeout: float) -> tuple[int, Optional[Any], str]:
    request = Request(url, headers=_headers(), method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            status = int(response.getcode())
            body = _read_body(response)
    except HTTPError as exc:
        return int(exc.code), None, exc.read(1024 * 1024).decode("utf-8", errors="replace")
    except (URLError, TimeoutError, OSError) as exc:
        raise HTTPCheckError(str(exc)) from exc
    parsed: Optional[Any] = None
    if body:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = None
    return status, parsed, body


def _post_chat(base_url: str, model: str, timeout: float, stream: bool) -> tuple[int, Optional[Any], str, float]:
    payload = {"model": model, "messages": [{"role": "user", "content": SMOKE_PROMPT}], "temperature": 0, "max_tokens": 32, "stream": stream}
    request = Request(_chat_url(base_url), data=json.dumps(payload).encode("utf-8"), headers=_headers(), method="POST")
    started = time.monotonic()
    try:
        with urlopen(request, timeout=timeout) as response:
            status = int(response.getcode())
            body = _read_body(response)
    except HTTPError as exc:
        return int(exc.code), None, exc.read(1024 * 1024).decode("utf-8", errors="replace"), time.monotonic() - started
    except (URLError, TimeoutError, OSError) as exc:
        raise HTTPCheckError(str(exc)) from exc
    parsed: Optional[Any] = None
    if body:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = None
    return status, parsed, body, time.monotonic() - started


def _extract_message_text(data: Any) -> str:
    try:
        return str(data["choices"][0]["message"]["content"] or "")
    except (KeyError, IndexError, TypeError):
        return ""


def _rough_token_count(text: str) -> int:
    if not text.strip():
        return 0
    return max(1, round(len(text.split()) * 1.3))


def _experience(total_latency: Optional[float], ttft: Optional[float], streaming: str, reachable: bool) -> str:
    if not reachable:
        return "Endpoint/config problem"
    if ttft is not None:
        if ttft <= 1.5:
            return "Good for interactive demo"
        if ttft <= 3.0:
            return "Acceptable but could feel slow"
        return "Likely frustrating without progress feedback"
    if total_latency is not None:
        if total_latency <= 4.0:
            return "Good for short non-streaming demo"
        if total_latency <= 10.0:
            return "Acceptable but streaming is recommended"
        return "Likely frustrating without streaming"
    if streaming == "no":
        return "Likely frustrating without streaming"
    return "Inconclusive"


def _base_suggestions(result: PerfResult) -> List[str]:
    suggestions: List[str] = []
    if not result.reachable:
        suggestions.append("Verify the endpoint URL, port, container networking, and whether the runtime is running.")
    if result.openai_compatible != "yes":
        suggestions.append("Check the OpenAI-compatible base URL. Many local runtimes expect the base URL to end with /v1.")
    if result.streaming_supported == "no":
        suggestions.append("Enable streaming or update the client/server path before a customer-facing demo.")
    if result.ttft_seconds is not None and result.ttft_seconds > 2.0:
        suggestions.append("Warm up the endpoint before demos and consider a smaller model or shorter context to improve TTFT.")
    if result.total_latency_seconds is not None and result.total_latency_seconds > 8.0:
        suggestions.append("Reduce prompt/context size, use streaming, or choose a smaller/quantized model for interactive UX.")
    if not suggestions:
        suggestions.append("Use this as a smoke signal only. Run real load tests separately before production claims.")
    suggestions.append("Next: inferdoctor optimize endpoint --ttft {0} --latency {1}".format("{0:.2f}".format(result.ttft_seconds) if result.ttft_seconds is not None else "0", "{0:.2f}".format(result.total_latency_seconds) if result.total_latency_seconds is not None else "0"))
    return suggestions


def _with_suggestions(result: PerfResult) -> PerfResult:
    return PerfResult(result.mode, result.endpoint, result.model, result.reachable, result.openai_compatible, result.streaming_supported, result.ttft_seconds, result.total_latency_seconds, result.rough_tokens_per_second, result.output_tokens_estimate, _experience(result.total_latency_seconds, result.ttft_seconds, result.streaming_supported, result.reachable), result.checks, _base_suggestions(result), result.raw_data)


def run_endpoint_smoke(endpoint: str, model: Optional[str] = None, timeout: float = 30.0) -> PerfResult:
    endpoint = endpoint.rstrip("/")
    checks: List[PerfCheck] = []
    raw: Dict[str, Any] = {"endpoint": endpoint, "timeout": timeout, "smoke_test": True}
    models_url = _models_url(endpoint)
    try:
        status, models_json, models_body = _get_json(models_url, timeout)
    except HTTPCheckError as exc:
        check = PerfCheck("reachability", "FAIL", describe_http_error(exc), [models_url])
        return _with_suggestions(PerfResult("endpoint", endpoint, model, False, "no", checks=[check], raw_data=raw))
    raw["models_status"] = status
    if status < 200 or status >= 300:
        return _with_suggestions(PerfResult("endpoint", endpoint, model, True, "no", checks=[_http_error_check(models_url, status, models_body)], raw_data=raw))
    if not isinstance(models_json, dict) or not isinstance(models_json.get("data"), list):
        check = PerfCheck("openai-compatible", "WARN", "/models did not return an OpenAI-compatible data list.", [models_url])
        return _with_suggestions(PerfResult("endpoint", endpoint, model, True, "no", checks=[check], raw_data=raw))
    checks.append(PerfCheck("models", "PASS", "/models returned {0} model(s).".format(len(models_json["data"]))))
    if not model:
        return _with_suggestions(PerfResult("endpoint", endpoint, None, True, "yes", checks=checks, raw_data=raw))
    try:
        status, chat_json, chat_body, latency = _post_chat(endpoint, model, timeout, stream=False)
    except HTTPCheckError as exc:
        checks.append(PerfCheck("chat-completions", "FAIL", describe_http_error(exc), [_chat_url(endpoint)]))
        return _with_suggestions(PerfResult("endpoint", endpoint, model, True, "yes", checks=checks, raw_data=raw))
    raw["chat_status"] = status
    if status < 200 or status >= 300:
        checks.append(_http_error_check(_chat_url(endpoint), status, chat_body))
        return _with_suggestions(PerfResult("endpoint", endpoint, model, True, "yes", total_latency_seconds=latency, checks=checks, raw_data=raw))
    text = _extract_message_text(chat_json)
    estimated_tokens = _rough_token_count(text)
    tps = (estimated_tokens / latency) if latency > 0 and estimated_tokens else None
    checks.append(PerfCheck("chat-completions", "PASS", "Tiny chat completion returned successfully."))
    return _with_suggestions(PerfResult("endpoint", endpoint, model, True, "yes", "unknown", None, latency, tps, estimated_tokens or None, checks=checks, raw_data=raw))


def run_streaming_smoke(endpoint: str, model: str, timeout: float = 30.0) -> PerfResult:
    endpoint = endpoint.rstrip("/")
    checks: List[PerfCheck] = []
    raw: Dict[str, Any] = {"endpoint": endpoint, "timeout": timeout, "smoke_test": True, "stream": True}
    models_url = _models_url(endpoint)
    try:
        status, models_json, models_body = _get_json(models_url, timeout)
    except HTTPCheckError as exc:
        check = PerfCheck("reachability", "FAIL", describe_http_error(exc), [models_url])
        return _with_suggestions(PerfResult("streaming", endpoint, model, False, "no", checks=[check], raw_data=raw))
    raw["models_status"] = status
    if status < 200 or status >= 300:
        return _with_suggestions(PerfResult("streaming", endpoint, model, True, "no", checks=[_http_error_check(models_url, status, models_body)], raw_data=raw))
    if not isinstance(models_json, dict) or not isinstance(models_json.get("data"), list):
        return _with_suggestions(PerfResult("streaming", endpoint, model, True, "no", checks=[PerfCheck("openai-compatible", "WARN", "/models did not return an OpenAI-compatible data list.")], raw_data=raw))
    checks.append(PerfCheck("models", "PASS", "/models returned {0} model(s).".format(len(models_json["data"]))))
    payload = {"model": model, "messages": [{"role": "user", "content": SMOKE_PROMPT}], "temperature": 0, "max_tokens": 32, "stream": True}
    request = Request(_chat_url(endpoint), data=json.dumps(payload).encode("utf-8"), headers=_headers(), method="POST")
    started = time.monotonic()
    first_chunk: Optional[float] = None
    chunks = 0
    text_parts: List[str] = []
    try:
        with urlopen(request, timeout=timeout) as response:
            status = int(response.getcode())
            if status < 200 or status >= 300:
                body = _read_body(response)
                checks.append(_http_error_check(_chat_url(endpoint), status, body))
                return _with_suggestions(PerfResult("streaming", endpoint, model, True, "yes", total_latency_seconds=time.monotonic() - started, checks=checks, raw_data=raw))
            while True:
                line = response.readline()
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace").strip()
                if not decoded or not decoded.startswith("data:"):
                    continue
                payload_text = decoded[5:].strip()
                if payload_text == "[DONE]":
                    break
                if first_chunk is None:
                    first_chunk = time.monotonic() - started
                chunks += 1
                try:
                    data = json.loads(payload_text)
                    delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if delta:
                        text_parts.append(str(delta))
                except (json.JSONDecodeError, AttributeError, IndexError):
                    pass
    except HTTPError as exc:
        checks.append(_http_error_check(_chat_url(endpoint), int(exc.code), exc.read(1024 * 1024).decode("utf-8", errors="replace")))
        return _with_suggestions(PerfResult("streaming", endpoint, model, True, "yes", total_latency_seconds=time.monotonic() - started, checks=checks, raw_data=raw))
    except (URLError, TimeoutError, OSError) as exc:
        checks.append(PerfCheck("streaming", "FAIL", describe_http_error(HTTPCheckError(str(exc))), [_chat_url(endpoint)]))
        return _with_suggestions(PerfResult("streaming", endpoint, model, True, "yes", checks=checks, raw_data=raw))
    total = time.monotonic() - started
    if first_chunk is None:
        checks.append(PerfCheck("streaming", "WARN", "No streamed data chunks were observed.", ["The server may ignore stream=true or buffer responses."]))
        return _with_suggestions(PerfResult("streaming", endpoint, model, True, "yes", "no", total_latency_seconds=total, checks=checks, raw_data=raw))
    text = "".join(text_parts)
    estimated_tokens = _rough_token_count(text)
    tps = (estimated_tokens / max(total - first_chunk, 0.001)) if estimated_tokens else None
    checks.append(PerfCheck("streaming", "PASS", "First streamed chunk arrived."))
    return _with_suggestions(PerfResult("streaming", endpoint, model, True, "yes", "yes", first_chunk, total, tps, estimated_tokens or None, checks=checks, raw_data={**raw, "stream_chunks": chunks}))


def _fmt_seconds(value: Optional[float]) -> str:
    return "unknown" if value is None else "{0:.2f}s".format(value)


def _fmt_rate(value: Optional[float]) -> str:
    return "unknown" if value is None else "~{0:.1f} tokens/sec".format(value)


def render_perf_result(result: PerfResult) -> str:
    lines = [
        "InferDoctor Performance UX Smoke Test",
        "=" * 57,
        "Mode: {0}".format(result.mode),
        "Endpoint: {0}".format(result.endpoint),
        "Model: {0}".format(result.model or "not provided"),
        "Reachable: {0}".format("yes" if result.reachable else "no"),
        "OpenAI-compatible check: {0}".format(result.openai_compatible),
        "Streaming supported: {0}".format(result.streaming_supported),
        "TTFT: {0}".format(_fmt_seconds(result.ttft_seconds)),
        "Total latency: {0}".format(_fmt_seconds(result.total_latency_seconds)),
        "Rough output speed: {0}".format(_fmt_rate(result.rough_tokens_per_second)),
        "User experience read: {0}".format(result.user_experience),
        "",
        "Checks:",
    ]
    for check in result.checks:
        lines.append("- [{0}] {1}: {2}".format(check.status, check.name, check.summary))
        for detail in check.details:
            lines.append("  - {0}".format(detail))
    lines.extend(["", "Top optimization suggestions:"])
    for index, suggestion in enumerate(result.suggestions, start=1):
        lines.append("{0}. {1}".format(index, suggestion))
    lines.extend(["", "Note: This is a timeout-bounded smoke test, not a benchmark. Results vary by prompt, model, runtime, cache state, and hardware."])
    return "\n".join(lines)
