from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class HTTPCheckError(ConnectionError):
    pass


@dataclass
class HTTPResponse:
    url: str
    status: int
    body: str
    json_data: Optional[Any] = None


def get_url(url: str, timeout: float = 2.0) -> HTTPResponse:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "InferDoctor/0.1",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            status = int(response.getcode())
            body = response.read(1024 * 1024).decode("utf-8", errors="replace")
    except HTTPError as exc:
        status = int(exc.code)
        body = exc.read(1024 * 1024).decode("utf-8", errors="replace")
    except (URLError, TimeoutError, OSError) as exc:
        raise HTTPCheckError(str(exc)) from exc

    parsed = None
    if body:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            pass
    return HTTPResponse(url=url, status=status, body=body, json_data=parsed)


def response_raw_data(response: HTTPResponse) -> Dict[str, Any]:
    raw: Dict[str, Any] = {
        "url": response.url,
        "http_status": response.status,
    }
    if response.json_data is not None:
        raw["response"] = response.json_data
    elif response.body:
        raw["response_preview"] = response.body[:500]
    return raw


def describe_http_error(error: HTTPCheckError) -> str:
    message = str(error)
    lowered = message.lower()
    if "connection refused" in lowered:
        return (
            "Connection refused. The service may not be running or listening "
            "at this address."
        )
    if "timed out" in lowered or "timeout" in lowered:
        return (
            "The request timed out. Increase --timeout or check whether the "
            "service is responsive."
        )
    if (
        "name or service not known" in lowered
        or "temporary failure in name resolution" in lowered
        or "nodename nor servname" in lowered
    ):
        return "The endpoint hostname could not be resolved."
    return message


def join_url(base_url: str, path: str) -> str:
    return "{0}/{1}".format(base_url.rstrip("/"), path.lstrip("/"))
