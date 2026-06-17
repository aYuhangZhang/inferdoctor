from unittest.mock import patch

import pytest

from inferdoctor.checkers.dify import DifyChecker
from inferdoctor.checkers.openwebui import OpenWebUIChecker
from inferdoctor.checkers.xinference import XinferenceChecker
from inferdoctor.core.config import Config
from inferdoctor.core.http import HTTPResponse
from inferdoctor.core.models import Status


@pytest.mark.parametrize(
    ("checker", "expected_url"),
    [
        (XinferenceChecker(), "http://127.0.0.1:9997/v1/models"),
        (DifyChecker(), "http://127.0.0.1:5001/"),
        (OpenWebUIChecker(), "http://127.0.0.1:3000/"),
    ],
)
@patch("inferdoctor.checkers.endpoint.get_url")
def test_endpoint_checkers_pass_on_success(get, checker, expected_url):
    get.return_value = HTTPResponse(
        url=expected_url,
        status=200,
        body="{}",
        json_data={},
    )

    result = checker.run(Config())

    assert result.status == Status.PASS
    get.assert_called_once_with(expected_url, timeout=2.0)


@patch("inferdoctor.checkers.endpoint.get_url")
def test_authenticated_endpoint_warns_but_is_reachable(get):
    get.return_value = HTTPResponse(
        url="http://127.0.0.1:5001/",
        status=401,
        body="unauthorized",
    )

    result = DifyChecker().run(Config())

    assert result.status == Status.WARN
    assert result.raw_data["reachable"] is True
