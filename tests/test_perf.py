
from __future__ import annotations

import json
from urllib.error import URLError

from inferdoctor.core import perf
from inferdoctor.core.perf import render_perf_result, run_endpoint_smoke, run_streaming_smoke


class FakeResponse:
    def __init__(self, status=200, body="", lines=None):
        self.status = status
        self.body = body.encode("utf-8")
        self.lines = [line.encode("utf-8") for line in (lines or [])]
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
    assert result.user_experience == "Endpoint/config problem"
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
            ]
        )

    monkeypatch.setattr(perf, "urlopen", fake_urlopen)

    result = run_streaming_smoke("http://127.0.0.1:8000/v1", "local-model", timeout=3)

    assert result.streaming_supported == "yes"
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

    assert result.streaming_supported == "no"
    assert any("No streamed data chunks" in check.summary for check in result.checks)
