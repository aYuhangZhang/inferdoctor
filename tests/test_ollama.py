from unittest.mock import patch

from inferdoctor.checkers.ollama import OllamaChecker
from inferdoctor.core.config import Config
from inferdoctor.core.http import HTTPCheckError, HTTPResponse
from inferdoctor.core.models import Status


@patch("inferdoctor.checkers.ollama.shutil.which", return_value=None)
@patch(
    "inferdoctor.checkers.ollama.get_url",
    side_effect=HTTPCheckError("connection refused"),
)
def test_ollama_checker_skips_when_not_installed_or_running(get, which):
    result = OllamaChecker().run(Config())

    assert result.status == Status.SKIP
    assert result.raw_data["reachable"] is False
    get.assert_called_once()
    which.assert_called_once_with("ollama")


@patch("inferdoctor.checkers.ollama.shutil.which", return_value="/usr/bin/ollama")
@patch("inferdoctor.checkers.ollama.get_url")
def test_ollama_checker_detects_cli_and_api(get, which):
    get.return_value = HTTPResponse(
        url="http://127.0.0.1:11434/api/tags",
        status=200,
        body='{"models": [{"name": "test"}]}',
        json_data={"models": [{"name": "test"}]},
    )

    result = OllamaChecker().run(Config())

    assert result.status == Status.PASS
    assert result.raw_data["model_count"] == 1
    get.assert_called_once()
    which.assert_called_once_with("ollama")
