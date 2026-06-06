from inferdoctor.checkers.endpoint import EndpointChecker


class DifyChecker(EndpointChecker):
    name = "dify"
    endpoint_name = "dify"
    probe_path = ""
    service_label = "Dify"
    offline_suggestions = [
        "Start Dify or update endpoints.dify to its API or web base URL.",
        "Check container port mappings if Dify is running in Docker.",
    ]
