from unittest.mock import patch

import pytest

from inferdoctor.checkers.llamacpp import LlamaCppChecker
from inferdoctor.checkers.lmstudio import LMStudioChecker
from inferdoctor.checkers.sglang import SGLangChecker
from inferdoctor.checkers.vllm import VLLMChecker
from inferdoctor.core.config import Config
from inferdoctor.core.http import HTTPCheckError, HTTPResponse
from inferdoctor.core.models import Status


@pytest.mark.parametrize(
    ("checker", "expected_url"),
    [
        (VLLMChecker(), "http://127.0.0.1:8000/v1/models"),
        (SGLangChecker(), "http://127.0.0.1:30000/v1/models"),
        (LlamaCppChecker(), "http://127.0.0.1:8080/v1/models"),
        (LMStudioChecker(), "http://127.0.0.1:1234/v1/models"),
    ],
)
@patch("inferdoctor.checkers.openai_compatible.get_url")
def test_openai_checker_accepts_models_response(get, checker, expected_url):
    get.return_value = HTTPResponse(
        url=expected_url,
        status=200,
        body='{"object": "list", "data": [{"id": "model"}]}',
        json_data={"object": "list", "data": [{"id": "model"}]},
    )

    result = checker.run(Config())

    assert result.status == Status.PASS
    assert result.raw_data["model_count"] == 1
    get.assert_called_once_with(expected_url, timeout=2.0)


@patch(
    "inferdoctor.checkers.openai_compatible.get_url",
    side_effect=HTTPCheckError("connection refused"),
)
def test_openai_checker_skips_offline_service(get):
    result = SGLangChecker().run(Config())

    assert result.status == Status.SKIP
    assert result.raw_data["reachable"] is False
    assert "--endpoint" in result.suggestions[1]


@patch("inferdoctor.checkers.openai_compatible.get_url")
def test_openai_checker_explains_unauthorized(get):
    get.return_value = HTTPResponse(
        url="http://127.0.0.1:8000/v1/models",
        status=401,
        body='{"error": "unauthorized"}',
        json_data={"error": "unauthorized"},
    )

    result = VLLMChecker().run(Config())

    assert result.status == Status.WARN
    assert "requires authentication" in result.summary
    assert "Set an API key" in result.suggestions[0]


@patch("inferdoctor.checkers.openai_compatible.get_url")
def test_openai_checker_suggests_v1_for_404(get):
    get.return_value = HTTPResponse(
        url="http://127.0.0.1:8000/v1/models",
        status=404,
        body="not found",
    )
    config = Config()
    config.endpoints["vllm"] = "http://127.0.0.1:8000"

    result = VLLMChecker().run(config)

    assert result.status == Status.WARN
    assert "Try adding /v1" in result.suggestions[1]
    assert "http://127.0.0.1:8000/v1" in result.suggestions[2]


@patch("inferdoctor.checkers.openai_compatible.get_url")
def test_openai_checker_warns_on_invalid_json(get):
    get.return_value = HTTPResponse(
        url="http://127.0.0.1:30000/v1/models",
        status=200,
        body="<html>dashboard</html>",
        json_data=None,
    )

    result = SGLangChecker().run(Config())

    assert result.status == Status.WARN
    assert "invalid JSON" in result.summary


@patch("inferdoctor.checkers.openai_compatible.get_url")
def test_openai_checker_warns_on_wrong_json_shape(get):
    get.return_value = HTTPResponse(
        url="http://127.0.0.1:8000/v1/models",
        status=200,
        body='{"models": []}',
        json_data={"models": []},
    )

    result = VLLMChecker().run(Config())

    assert result.status == Status.WARN
    assert "not OpenAI-compatible" in result.summary
