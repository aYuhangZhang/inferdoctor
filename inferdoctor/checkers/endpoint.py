from __future__ import annotations

from typing import List

from inferdoctor.core.checker import Checker
from inferdoctor.core.config import Config
from inferdoctor.core.http import (
    HTTPCheckError,
    describe_http_error,
    get_url,
    join_url,
    response_raw_data,
)
from inferdoctor.core.models import CheckResult, Status


class EndpointChecker(Checker):
    endpoint_name: str
    probe_path: str
    service_label: str
    offline_suggestions: List[str]

    def run(self, config: Config) -> CheckResult:
        base_url = config.endpoints[self.endpoint_name]
        url = join_url(base_url, self.probe_path)
        try:
            response = get_url(url, timeout=config.timeout)
        except HTTPCheckError as exc:
            return CheckResult(
                name=self.name,
                status=Status.SKIP,
                summary="{0} endpoint is not reachable".format(self.service_label),
                details=["{0}: {1}".format(url, describe_http_error(exc))],
                suggestions=self.offline_suggestions,
                raw_data={"url": url, "reachable": False},
            )

        raw_data = response_raw_data(response)
        raw_data["reachable"] = True
        if 200 <= response.status < 300:
            return CheckResult(
                name=self.name,
                status=Status.PASS,
                summary="{0} endpoint is reachable".format(self.service_label),
                details=["{0} returned HTTP {1}.".format(url, response.status)],
                raw_data=raw_data,
            )

        if response.status in (401, 403):
            return CheckResult(
                name=self.name,
                status=Status.WARN,
                summary="{0} endpoint requires authentication".format(
                    self.service_label
                ),
                details=["{0} returned HTTP {1}.".format(url, response.status)],
                suggestions=[
                    "The service is reachable; configure credentials in the client that uses it."
                ],
                raw_data=raw_data,
            )

        return CheckResult(
            name=self.name,
            status=Status.WARN,
            summary="{0} responded with HTTP {1}".format(
                self.service_label, response.status
            ),
            details=["Probe URL: {0}".format(url)],
            suggestions=[
                "Verify the configured base URL and inspect the service logs."
            ],
            raw_data=raw_data,
        )
