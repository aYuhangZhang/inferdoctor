from inferdoctor.checkers.endpoint import EndpointChecker


class XinferenceChecker(EndpointChecker):
    name = "xinference"
    endpoint_name = "xinference"
    probe_path = "v1/models"
    service_label = "Xinference"
    offline_suggestions = [
        "Start Xinference or update endpoints.xinference.",
        "Confirm the supervisor is listening on the configured host and port.",
        "No Xinference SDK is required for this check.",
    ]
