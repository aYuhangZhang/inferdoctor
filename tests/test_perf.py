
from __future__ import annotations

import json
from urllib.error import URLError

from inferdoctor.core import perf
from inferdoctor.core.perf import render_perf_result, run_endpoint_smoke, run_streaming_smoke


class FakeResponse:
    def __init__(self, status=200, body="", lines=None, content_type="application/json"):
        self.status = status
        self.body = body.encode("utf-8")
        self.lines = [line.encode("utf-8") for line in (lines or [])]
        self.headers = {"Content-Type": content_type}
        self.index = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def getcode(self):
        return self.status

    def read(self, _size=-1):
        return self.body

    def readline(self):
        if self.index >= len(self.lines):
            return b""
        line = self.lines[self.index]
        self.index += 1
        return line


def test_perf_endpoint_success_mock(monkeypatch):
    calls = []

    def fake_urlopen(request, timeout):
        calls.append(request.full_url)
        if request.full_url.endswith("/models"):
            return FakeResponse(body=json.dumps({"data": [{"id": "local-model"}]}))
        payload = json.loads(request.data.decode("utf-8"))
        assert payload["model"] == "local-model"
        assert payload["stream"] is False
        return FakeResponse(body=json.dumps({"choices": [{"message": {"content": "Smoke test ok."}}]}))

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_endpoint_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=3)
    rendered = render_perf_result(result)

    assert result.reachable is True
    assert result.openai_compatible == "yes"
    assert result.total_latency_seconds is not None
    assert result.output_tokens_estimate is not None
    assert "Performance UX Smoke Test" in rendered
    assert len(calls) == 2


def test_perf_endpoint_timeout_mock(monkeypatch):
    def fake_urlopen(request, timeout):
        raise URLError("timed out")

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_endpoint_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=1)

    assert result.reachable is False
    assert result.openai_compatible == "no"
    assert result.user_experience == "Endpoint/configuration failure"
    assert "time" in result.checks[0].summary.lower()


def test_perf_streaming_first_chunk_mock(monkeypatch):
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/models"):
            return FakeResponse(body=json.dumps({"data": [{"id": "local-model"}]}))
        payload = json.loads(request.data.decode("utf-8"))
        assert payload["stream"] is True
        return FakeResponse(
            lines=[
                "data: {\"choices\":[{\"delta\":{\"content\":\"Hello\"}}]}\n",
                "data: {\"choices\":[{\"delta\":{\"content\":\" world\"}}]}\n",
                "data: [DONE]\n",
            ],
            content_type="text/event-stream",
        )

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_streaming_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=3)

    assert result.streaming_supported == "confirmed"
    assert result.ttft_seconds is not None
    assert result.total_latency_seconds is not None
    assert result.output_tokens_estimate is not None


def test_perf_streaming_unsupported_mock(monkeypatch):
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/models"):
            return FakeResponse(body=json.dumps({"data": [{"id": "local-model"}]}))
        return FakeResponse(body=json.dumps({"choices": [{"message": {"content": "not streamed"}}]}))

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_streaming_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=3)

    assert result.streaming_supported == "accepted_full_response"
    assert result.successful_runs == 1



def test_streaming_ignores_role_only_and_empty_chunks(monkeypatch):
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/models"):
            return FakeResponse(body=json.dumps({"data": [{"id": "local-model"}]}))
        return FakeResponse(
            lines=[
                ": keepalive\n",
                "\n",
                "data: {\"choices\":[{\"delta\":{\"role\":\"assistant\"}}]}\n",
                "data: {\"choices\":[{\"delta\":{\"content\":\"\"}}]}\n",
                "data: {\"choices\":[{\"delta\":{\"content\":\"Visible\"}}]}\n",
                "data: [DONE]\n",
            ],
            content_type="text/event-stream",
        )

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_streaming_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=3)

    assert result.streaming_supported == "confirmed"
    assert result.ttft_seconds is not None
    assert result.runs[0].content_chunks == 1


def test_streaming_no_content_is_not_success(monkeypatch):
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/models"):
            return FakeResponse(body=json.dumps({"data": [{"id": "local-model"}]}))
        return FakeResponse(
            lines=[
                "data: {\"choices\":[{\"delta\":{\"role\":\"assistant\"}}]}\n",
                "data: [DONE]\n",
            ],
            content_type="text/event-stream",
        )

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_streaming_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=3)

    assert result.streaming_supported == "no_content"
    assert result.failed_runs == 1
    assert result.ttft_seconds is None


def test_streaming_uses_usage_tokens_for_exact_tps(monkeypatch):
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/models"):
            return FakeResponse(body=json.dumps({"data": [{"id": "local-model"}]}))
        return FakeResponse(
            lines=[
                "data: {\"choices\":[{\"delta\":{\"content\":\"Hello\"}}]}\n",
                "data: {\"choices\":[{\"delta\":{}}],\"usage\":{\"completion_tokens\":3}}\n",
                "data: [DONE]\n",
            ],
            content_type="text/event-stream",
        )

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_streaming_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=3)

    assert result.metric_quality["tokens"] == "exact"
    assert result.tps_quality == "exact"
    assert result.output_tokens_exact == 3


def test_http_200_error_object_fails_without_body_leak(monkeypatch):
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/models"):
            return FakeResponse(body=json.dumps({"data": [{"id": "local-model"}]}))
        return FakeResponse(body=json.dumps({"error": {"message": "bad api key secret-value-123456"}}))

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_endpoint_smoke("http://user:pass@127.0.0.1:8000/v1?api_key=secret", "local-model", timeout=3)

    assert result.failed_runs == 1
    assert "user:pass" not in result.endpoint
    assert "secret" not in result.endpoint
