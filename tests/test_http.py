from inferdoctor.core.http import HTTPCheckError, describe_http_error


def test_connection_refused_error_is_actionable():
    message = describe_http_error(
        HTTPCheckError("<urlopen error [Errno 111] Connection refused>")
    )

    assert "service may not be running" in message
    assert "another port" in message


def test_timeout_error_mentions_cli_override():
    message = describe_http_error(HTTPCheckError("request timed out"))

    assert "--timeout" in message
    assert "loading" in message
